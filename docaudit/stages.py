"""Deterministic stages. Both runners call exactly these functions.

prepare -> [agents: readers, cross-reference checker] -> verify
        -> [agent: gap reader] -> verify -> [agents: skeptics]
        -> recheck_prep -> [agent: recheck skeptic] -> aggregate
        -> [agent: editor] -> report
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from .aggregate import aggregate
from .align import Alignment, align
from .ingest import Document, ingest_file
from .merge import coverage, merge_findings, same_issue
from .render import (render_audit_chunk, render_diff_chunk, render_document, render_editor_input,
                     render_findings_batch, render_index, render_ops_list)
from .runstore import Run
from .sweeps import defined_terms, find_references, numeric_facts, sweep_findings
from .verify import DocIndex, VerifiedFinding, verification_stats, verify_finding

DEFAULTS = {
    "chunk_chars": 12000,
    "skeptic_batch_size": 12,
    "skeptic_batches": None,  # fixed number of batches (the workflow sets this)
    "skeptic_votes": 1,
    "low_confidence": 0.25,
}


def summary_line(obj: dict) -> str:
    """The one-line JSON summary every CLI stage prints last (workflow shell steps read it)."""
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


# ---------------------------------------------------------------- prepare


def _diff_chunks(a: Document, b: Document, alignment: Alignment, max_chars: int) -> list[dict]:
    groups: list[dict] = []
    current_key = None
    for op in alignment.ops:
        key = b.para(op.b).section if op.b else (current_key or a.para(op.a).section)
        if key != current_key:
            title = (b.section_of(op.b) if op.b else a.section_of(op.a)).title
            groups.append({"key": key, "title": title, "ops": [], "chars": 0, "changed": 0})
            current_key = key
        g = groups[-1]
        g["ops"].append(op.index)
        if op.op == "equal":
            g["chars"] += 100
        else:
            g["changed"] += 1
            g["chars"] += (len(a.para(op.a).text) if op.a else 0) + (len(b.para(op.b).text) if op.b else 0) + 60
    chunks: list[dict] = []

    def start() -> dict:
        c = {"ops": [], "titles": [], "chars": 0}
        chunks.append(c)
        return c

    cur = None
    for g in groups:
        if g["changed"] == 0:
            continue  # unchanged sections need no reader
        if cur is None or (cur["chars"] + g["chars"] > max_chars and cur["ops"]):
            cur = start()
        if g["chars"] > max_chars:
            # Split an oversized section at operation boundaries.
            for idx in g["ops"]:
                op = alignment.ops[idx]
                cost = 100 if op.op == "equal" else (len(a.para(op.a).text) if op.a else 0) + (len(b.para(op.b).text) if op.b else 0) + 60
                if cur["chars"] + cost > max_chars and cur["ops"]:
                    cur = start()
                cur["ops"].append(idx)
                cur["chars"] += cost
                if g["title"] not in cur["titles"]:
                    cur["titles"].append(g["title"])
            continue
        cur["ops"].extend(g["ops"])
        cur["chars"] += g["chars"]
        cur["titles"].append(g["title"])
    out = []
    for n, c in enumerate(chunks, start=1):
        paras_a = [alignment.ops[i].a for i in c["ops"] if alignment.ops[i].a and alignment.ops[i].op != "equal"]
        paras_b = [alignment.ops[i].b for i in c["ops"] if alignment.ops[i].b and alignment.ops[i].op != "equal"]
        out.append({"id": f"c{n:02d}", "file": f"chunks/c{n:02d}.md", "ops": c["ops"], "titles": c["titles"],
                    "paras": {"A": paras_a, "B": paras_b}, "chars": c["chars"]})
    return out


def _audit_chunks(doc: Document, max_chars: int) -> list[dict]:
    chunks: list[dict] = []
    cur = None
    for sec in doc.sections:
        size = sum(len(doc.para(pid).text) + 20 for pid in sec.para_ids)
        if cur is None or (cur["chars"] + size > max_chars and cur["paras"]):
            cur = {"paras": [], "titles": [], "chars": 0}
            chunks.append(cur)
        for pid in sec.para_ids:
            cost = len(doc.para(pid).text) + 20
            if cur["chars"] + cost > max_chars and cur["paras"] and size > max_chars:
                cur = {"paras": [], "titles": [], "chars": 0}
                chunks.append(cur)
            cur["paras"].append(pid)
            cur["chars"] += cost
            if sec.title not in cur["titles"]:
                cur["titles"].append(sec.title)
    return [{"id": f"c{n:02d}", "file": f"chunks/c{n:02d}.md", "titles": c["titles"], "paras": {"A": c["paras"]},
             "chars": c["chars"]} for n, c in enumerate(chunks, start=1)]


def prepare(run_dir: str | Path, mode: str, a_path: str, b_path: str | None = None, label: str | None = None,
            python: str = "python", repo_dir: str | Path | None = None, **config) -> dict:
    if mode not in ("audit", "diff"):
        raise ValueError("mode must be 'audit' or 'diff'")
    if mode == "diff" and not b_path:
        raise ValueError("diff mode needs --b")
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in config.items() if v is not None})
    run = Run(run_dir)
    run.root.mkdir(parents=True, exist_ok=True)
    docs = {"A": ingest_file(a_path, "A")}
    if mode == "diff":
        docs["B"] = ingest_file(b_path, "B")
    for key, doc in docs.items():
        run.write_json(f"docs/{key}.json", doc.to_dict())
        run.write_text(f"docs/{key}.md", render_document(doc))

    alignment = None
    if mode == "diff":
        alignment = align(docs["A"], docs["B"])
        run.write_json("alignment.json", alignment.to_dict())
        sweeps = sweep_findings(docs["B"], baseline_doc=docs["A"])
        chunks = _diff_chunks(docs["A"], docs["B"], alignment, cfg["chunk_chars"])
        for c in chunks:
            run.write_text(c["file"], render_diff_chunk(c, alignment, docs))
    else:
        sweeps = sweep_findings(docs["A"])
        chunks = _audit_chunks(docs["A"], cfg["chunk_chars"])
        for c in chunks:
            run.write_text(c["file"], render_audit_chunk(c, docs["A"]))
    run.write_json("sweeps.json", {"findings": sweeps})

    refs = {k: [{"para_id": r.para_id, "text": r.text, "status": r.status, "detail": r.detail} for r in find_references(d)] for k, d in docs.items()}
    terms = {k: defined_terms(d) for k, d in docs.items()}
    numbers = {k: numeric_facts(d) for k, d in docs.items()}
    run.write_text("index.md", render_index(mode, docs, alignment, refs, terms, numbers, sweeps))

    plan = {
        "schema_version": 1,
        "mode": mode,
        "label": label or run.root.name,
        "docs": {k: {"source": d.source, "sha256": d.sha256, "format": d.format, "paragraphs": len(d.paragraphs),
                     "sections": len(d.sections)} for k, d in docs.items()},
        "alignment": alignment.stats() if alignment else None,
        "chunks": chunks,
        "config": cfg,
    }
    run.write_json("plan.json", plan)
    # The only file with absolute paths; run directories are not committed.
    run.write_json("workflow_args.json", {
        "runDir": run.root.resolve().as_posix(),
        "repoDir": Path(repo_dir or Path.cwd()).resolve().as_posix(),
        "python": python,
        "mode": mode,
        "chunks": [c["id"] for c in chunks],
        "skepticBatches": cfg["skeptic_batches"],
        "skepticVotes": cfg["skeptic_votes"],
    })
    return {"stage": "prepare", "mode": mode, "chunks": len(chunks), "sweep_findings": len(sweeps),
            "paragraphs": {k: len(d.paragraphs) for k, d in docs.items()}}


# ---------------------------------------------------------------- verify


def _collect(run: Run, patterns: list[str]) -> tuple[list[tuple[str, dict]], list[dict]]:
    raws: list[tuple[str, dict]] = []
    failures: list[dict] = []
    for pattern in patterns:
        for label, obj in run.agent_outputs(pattern):
            if "_error" in obj or not isinstance(obj.get("findings"), list):
                failures.append({"agent": label, "error": obj.get("_error", "no findings list")})
                continue
            for f in obj["findings"]:
                raws.append((label, f))
    return raws, failures


def _split_batches(findings: list[dict], n_batches: int) -> list[list[dict]]:
    n_batches = max(1, n_batches)
    out: list[list[dict]] = [[] for _ in range(n_batches)]
    if not findings:
        return out
    per = math.ceil(len(findings) / n_batches)
    for i, f in enumerate(findings):
        out[min(n_batches - 1, i // per)].append(f)
    return out


def verify(run_dir: str | Path) -> dict:
    run = Run(run_dir)
    docs, alignment, mode = run.docs, run.alignment, run.mode
    index = DocIndex(docs)
    raws, failures = _collect(run, ["reader-*.json", "crossref.json", "gap.json"])
    verified: list[VerifiedFinding] = [verify_finding(f, src, mode, index) for src, f in raws]
    for f in run.read_json("sweeps.json")["findings"]:
        verified.append(verify_finding(f, "sweep", mode, index))
    accepted = [v for v in verified if v.status == "accepted"]
    merged = merge_findings(accepted, docs, alignment)
    merged_dicts = [m.to_dict() for m in merged]
    cov = coverage(alignment, merged_dicts) if alignment else None
    # Coverage of the first pass alone (everything except the gap reader), so
    # the report can show what the gap reader added whatever order stages ran in.
    first = [f for f in merged_dicts if any(s != "gap" for s in f["sources"])]
    cov_first = coverage(alignment, first) if alignment else None
    run.write_json("verified.json", {
        "stats": verification_stats(verified),
        "agent_failures": failures,
        "coverage_first_pass": cov_first,
        "coverage": cov,
        "findings": merged_dicts,
        "verification": [v.to_dict() for v in verified],
    })
    if alignment is not None:
        ops = [alignment.ops[i] for i in cov["uncovered"]]
        run.write_text("gaps.md", render_ops_list(
            "Uncovered changes",
            f"{len(ops)} of {cov['changed_ops']} changed operations are not cited by any accepted finding. "
            "Decide for each one: substantive (report it) or editorial (say so in coverage_note with the op number).",
            ops, docs))
        run.write_json("gaps.json", {"ops": cov["uncovered"]})
    cfg = run.plan["config"]
    n_batches = cfg.get("skeptic_batches") or max(1, math.ceil(len(merged_dicts) / cfg["skeptic_batch_size"]))
    for old in run.path("skeptic").glob("b*.*") if run.path("skeptic").exists() else []:
        old.unlink()
    batches = _split_batches(merged_dicts, n_batches)
    for n, batch in enumerate(batches, start=1):
        bid = f"b{n:02d}"
        run.write_json(f"skeptic/{bid}.json", {"batch": bid, "finding_ids": [f["id"] for f in batch]})
        run.write_text(f"skeptic/{bid}.md", render_findings_batch(f"Skeptic batch {bid}", batch, docs, alignment))
    stats = verification_stats(verified)
    # Only batches that hold findings are listed: both runners start one skeptic per
    # listed batch, so an empty batch never costs an agent call in either runner.
    non_empty = [f"b{n:02d}" for n, batch in enumerate(batches, start=1) if batch]
    return {"stage": "verify", "agent_findings": stats["agent_findings"], "rejected": stats["rejected"],
            "merged": len(merged_dicts), "batches": non_empty,
            "coverage": cov["ratio"] if cov else None, "uncovered": len(cov["uncovered"]) if cov else 0,
            "agent_failures": len(failures)}


# ---------------------------------------------------------------- recheck


def _as_verified(d: dict) -> VerifiedFinding:
    from .verify import EvidenceCheck
    checks = [EvidenceCheck(e["doc"], e["para_id"], e["quote"], True, e["match"], e["para_id"], e["relocated"]) for e in d["evidence"]]
    return VerifiedFinding(d.get("sources", ["?"])[0], d["kind"], d["title"], d["description"], d["severity"],
                           d["confidence"], checks, "accepted")


def recheck_prep(run_dir: str | Path) -> dict:
    """Verify the skeptics' 'missed' findings; attach duplicates, queue new ones for a recheck."""
    run = Run(run_dir)
    docs, alignment, mode = run.docs, run.alignment, run.mode
    index = DocIndex(docs)
    base = run.read_json("verified.json")["findings"]
    base_v = [_as_verified(f) for f in base]
    verified: list[VerifiedFinding] = []
    failures = []
    for label, obj in run.agent_outputs("skeptic-*.json"):
        if "_error" in obj or not isinstance(obj.get("missed"), list):
            failures.append({"agent": label, "error": obj.get("_error", "no missed list")})
            continue
        for f in obj["missed"]:
            verified.append(verify_finding(f, f"{label}:missed", mode, index))
    attached: list[dict] = []
    fresh: list[VerifiedFinding] = []
    for v in verified:
        if v.status != "accepted":
            continue
        dup = next((b for b, bv in zip(base, base_v) if same_issue(v, bv, docs)), None)
        if dup is not None:
            attached.append({"finding_id": dup["id"], "source": v.source, "title": v.title})
        else:
            fresh.append(v)
    start = len(base) + 1
    new = [m.to_dict() for m in merge_findings(fresh, docs, alignment, id_start=start)]
    run.write_json("verified_missed.json", {
        "stats": verification_stats(verified),
        "agent_failures": failures,
        "attached": attached,
        "findings": new,
        "verification": [v.to_dict() for v in verified],
    })
    run.write_json("skeptic/r01.json", {"batch": "r01", "finding_ids": [f["id"] for f in new]})
    run.write_text("skeptic/r01.md", render_findings_batch("Recheck batch r01 (findings the skeptics reported as missed)", new, docs, alignment))
    return {"stage": "recheck_prep", "missed_reported": len(verified), "missed_rejected": sum(v.status == "rejected" for v in verified),
            "attached_to_existing": len(attached), "recheck_findings": len(new)}


# ---------------------------------------------------------------- aggregate


def aggregate_stage(run_dir: str | Path) -> dict:
    run = Run(run_dir)
    index = DocIndex(run.docs)
    base = run.read_json("verified.json")["findings"]
    missed = run.read_json("verified_missed.json") if run.exists("verified_missed.json") else {"findings": [], "attached": []}
    findings = base + missed["findings"]
    for a in missed.get("attached", []):
        for f in findings:
            if f["id"] == a["finding_id"] and a["source"] not in f["sources"]:
                f["sources"] = sorted(f["sources"] + [a["source"]])
    raw_verdicts: list[tuple[str, dict]] = []
    failures = []
    for pattern in ("skeptic-*.json", "recheck-*.json"):
        for label, obj in run.agent_outputs(pattern):
            if "_error" in obj or not isinstance(obj.get("verdicts"), list):
                failures.append({"agent": label, "error": obj.get("_error", "no verdicts list")})
                continue
            raw_verdicts.extend((label, v) for v in obj["verdicts"])
    agg = aggregate(findings, raw_verdicts, index, low_confidence=run.plan["config"]["low_confidence"])
    agg["agent_failures"] = failures
    run.write_json("aggregated.json", agg)
    run.write_text("editor_input.md", render_editor_input(agg))
    return {"stage": "aggregate", "findings": len(agg["findings"]), "low_confidence": len(agg["low_confidence"]),
            "killed": len(agg["killed"]), "status_counts": agg["status_counts"]}
