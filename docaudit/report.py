"""Markdown + JSON report. Every finding links to the paragraphs it quotes."""

from __future__ import annotations

import re
from pathlib import Path

from . import __version__
from .runstore import Run
from .schemas import EDITOR_OUTPUT, validate
from .verify import DocIndex

_SUMMARY_QUOTE_RE = re.compile(r"[\"\u201c]([^\"\u201d]{8,400})[\"\u201d]")
_ID_RE = re.compile(r"\bF\d{3}\b")


def _anchor(doc: str, pid: str) -> str:
    return f"{doc}-{pid}"


def _link(doc: str, pid: str) -> str:
    return f"[{doc}:{pid}](#{_anchor(doc, pid).lower()})"


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def check_editor(editor: dict | None, agg: dict, index: DocIndex) -> dict:
    main_ids = [f["id"] for f in agg["findings"]]
    low_ids = {f["id"] for f in agg["low_confidence"]}
    killed_ids = {f["id"] for f in agg["killed"]}
    issues: list[str] = []
    if editor is None:
        return {"present": False, "executive_summary": "", "themes": [], "ordered_ids": main_ids,
                "issues": ["editor output missing: findings are listed in default order"], "unverified_quotes": []}
    errors = validate(editor, EDITOR_OUTPUT)
    if errors:
        return {"present": False, "executive_summary": "", "themes": [], "ordered_ids": main_ids,
                "issues": ["editor output invalid: " + "; ".join(errors[:3])], "unverified_quotes": []}
    known = set(main_ids) | low_ids
    ordered = []
    for fid in editor["ordered_finding_ids"]:
        if fid in killed_ids:
            issues.append(f"editor listed refuted finding {fid}; ignored")
        elif fid not in known:
            issues.append(f"editor listed unknown id {fid}; ignored")
        elif fid in set(main_ids) and fid not in ordered:
            ordered.append(fid)
    missing = [fid for fid in main_ids if fid not in ordered]
    if missing:
        issues.append(f"editor omitted {len(missing)} finding(s); appended in default order")
    ordered += missing
    themes = []
    for t in editor["themes"]:
        ids = [fid for fid in t["finding_ids"] if fid in known]
        dropped = [fid for fid in t["finding_ids"] if fid not in known]
        if dropped:
            issues.append(f"theme '{t['title']}' referenced unknown or refuted ids {', '.join(dropped)}; dropped")
        if ids:
            themes.append({"title": t["title"], "finding_ids": ids})
    for fid in sorted(set(_ID_RE.findall(editor["executive_summary"]))):
        if fid not in known:
            issues.append(f"summary mentions {fid}, which is not a surviving finding")
    unverified = []
    for q in _SUMMARY_QUOTE_RE.findall(editor["executive_summary"]):
        if len(q.split()) < 4:
            continue
        if not any(index.locate(k, q) for k in index.docs):
            unverified.append(q)
    if unverified:
        issues.append(f"{len(unverified)} quote(s) in the summary were not found in the documents")
    return {"present": True, "executive_summary": editor["executive_summary"].strip(), "themes": themes,
            "ordered_ids": ordered, "issues": issues, "unverified_quotes": unverified}


def build_report(run_dir: str | Path, runner: str = "unknown", backend: str = "unknown", model: str | None = None,
                 fixture: bool = False) -> dict:
    run = Run(run_dir)
    plan, docs = run.plan, run.docs
    index = DocIndex(docs)
    verified = run.read_json("verified.json")
    missed = run.read_json("verified_missed.json") if run.exists("verified_missed.json") else None
    agg = run.read_json("aggregated.json")
    editor = run.read_json("agents/editor.json") if run.exists("agents/editor.json") else None
    usage = run.read_json("usage.json") if run.exists("usage.json") else None
    run_log = run.read_json("run_log.json") if run.exists("run_log.json") else None
    ed = check_editor(editor, agg, index)

    by_id = {f["id"]: f for f in agg["findings"]}
    ordered = [by_id[i] for i in ed["ordered_ids"] if i in by_id]
    cited = set()
    for group in (ordered, agg["low_confidence"], agg["killed"]):
        for f in group:
            for e in f["evidence"]:
                cited.add((e["doc"], e["para_id"]))
            for v in f.get("verdicts", []):
                for e in v["counter_evidence"]:
                    if e.get("verified"):
                        cited.add((e["doc"], e["para_id"]))
    paragraphs = {}
    for doc_key, pid in sorted(cited, key=lambda k: (k[0], docs[k[0]].para(k[1]).index)):
        p = docs[doc_key].para(pid)
        sec = docs[doc_key].section_of(pid)
        paragraphs[f"{doc_key}:{pid}"] = {"text": p.text, "section": sec.title if sec else ""}

    rejected = [v for v in verified["verification"] if v["status"] == "rejected"]
    if missed:
        rejected += [v for v in missed["verification"] if v["status"] == "rejected"]
    failures = verified.get("agent_failures", []) + (missed or {}).get("agent_failures", []) + agg.get("agent_failures", [])
    if run_log:
        failures += run_log.get("failures", [])

    report = {
        "schema_version": 1,
        "run": {
            "label": plan["label"],
            "mode": plan["mode"],
            "runner": runner,
            "backend": backend,
            "model": model,
            "fixture": fixture,
            "docaudit_version": __version__,
            "docs": plan["docs"],
            "alignment": plan.get("alignment"),
            "chunks": len(plan["chunks"]),
        },
        "pipeline": {
            "verification": verified["stats"],
            "missed_verification": missed["stats"] if missed else None,
            "missed_attached_to_existing": len(missed["attached"]) if missed else 0,
            "merged_findings": len(verified["findings"]) + (len(missed["findings"]) if missed else 0),
            "coverage_first_pass": verified.get("coverage_first_pass"),
            "coverage": verified.get("coverage"),
            "skeptic": agg["verdict_stats"],
            "status_counts": agg["status_counts"],
            "agent_failures": failures,
            "incomplete": (run_log or {}).get("incomplete"),
            "usage": usage["totals"] if usage else None,
        },
        "summary": {k: ed[k] for k in ("executive_summary", "themes", "issues", "unverified_quotes")},
        "findings": ordered,
        "low_confidence": agg["low_confidence"],
        "killed": agg["killed"],
        "rejected": [{"source": v["source"], "kind": v["kind"], "title": v["title"], "code": v["code"], "reasons": v["reasons"]} for v in rejected],
        "paragraphs": paragraphs,
    }
    run.write_json("report.json", report)
    run.write_text("report.md", render_markdown(report))
    return report


def _finding_md(f: dict, show_verdicts: bool = True) -> list[str]:
    out = [f"### {f['id']} [{f['severity']}] {f['kind']}: {_md_escape(f['title'])}", ""]
    meta = f"Confidence {f['confidence']:.2f} ({f['status']}"
    if f.get("original_severity") and f["original_severity"] != f["severity"]:
        meta += f", severity lowered from {f['original_severity']}"
    meta += f"). Reported by {', '.join(f['sources'])}."
    out += [meta, "", f["description"], ""]
    for e in f["evidence"]:
        tag = e["match"] + (", re-attributed" if e.get("relocated") else "")
        out.append(f"- {_link(e['doc'], e['para_id'])} ({tag}): \"{e['quote']}\"")
    if show_verdicts:
        for v in f.get("verdicts", []):
            line = f"- Skeptic {v['source']}: **{v['effective']}**"
            if v["effective"] != v["verdict"]:
                line += f" (said {v['verdict']})"
            line += f". {v['reason']}"
            out.append(line)
            for e in v["counter_evidence"]:
                mark = "" if e.get("verified") else " (counter-quote NOT verified)"
                out.append(f"  - counter-evidence {_link(e['doc'], e['para_id'])}{mark}: \"{e['quote']}\"")
            for n in v.get("notes", []):
                out.append(f"  - note: {n}")
    out.append("")
    return out


def render_markdown(r: dict) -> str:
    run, pipe = r["run"], r["pipeline"]
    title = "Document diff report" if run["mode"] == "diff" else "Document audit report"
    out = [f"# {title}: {run['label']}", ""]
    if run["fixture"]:
        out += ["> **Fixture run.** Produced by the scripted FakeLLM test backend, not by a language model. "
                "It exercises every pipeline stage on real documents; the findings and verdicts are heuristic "
                "placeholders and say nothing about model quality.", ""]
    out += ["| | |", "|---|---|", f"| Mode | {run['mode']} |"]
    for k, d in run["docs"].items():
        out.append(f"| Document {k} | `{d['source']}` ({d['paragraphs']} paragraphs, sha256 `{d['sha256'][:12]}`) |")
    out.append(f"| Runner / backend | {run['runner']} / {run['backend']}" + (f" (`{run['model']}`)" if run["model"] else "") + " |")
    if run.get("alignment"):
        al = run["alignment"]
        out.append("| Alignment | " + ", ".join(f"{k} {v}" for k, v in al.items()) + " |")
    out.append("")

    v = pipe["verification"]
    sk = pipe["skeptic"]
    sc = pipe["status_counts"]
    out += ["## Pipeline", "", "| Stage | Result |", "|---|---|",
            f"| Section-reader chunks | {run['chunks']} |",
            f"| Findings emitted by agents | {v['agent_findings']} |",
            f"| Rejected by the quote verifier | {v['rejected']} ({v['rejection_rate']:.1%}) |",
            f"| Deterministic sweep findings | {v['sweep_findings']} |",
            f"| Evidence match levels (accepted) | {', '.join(f'{k} {n}' for k, n in v['evidence_match_levels'].items()) or '-'}; re-attributed {v['evidence_relocated']} |",
            f"| Findings after merge | {pipe['merged_findings']} |"]
    if pipe.get("coverage"):
        cov = pipe["coverage"]
        first = pipe.get("coverage_first_pass")
        prefix = f"first pass {first['covered']}/{first['changed_ops']} ({first['ratio']:.1%}); " if first else ""
        out.append(f"| Changed operations cited by a finding | {prefix}with gap reader {cov['covered']}/{cov['changed_ops']} ({cov['ratio']:.1%}) |")
    if pipe.get("missed_verification"):
        mv = pipe["missed_verification"]
        out.append(f"| Skeptic 'missed' findings | {mv['agent_findings']} reported, {mv['rejected']} rejected, "
                   f"{pipe['missed_attached_to_existing']} duplicates attached |")
    out.append(f"| Skeptic verdicts | {sk['verdicts']} ({', '.join(f'{k} {n}' for k, n in sk['by_effective'].items()) or '-'}); "
               f"ungrounded refutations {sk['ungrounded_refutations']} |")
    out.append(f"| Final status | {', '.join(f'{k} {n}' for k, n in sc.items()) or '-'} |")
    if pipe.get("usage"):
        u = pipe["usage"]
        out.append(f"| LLM calls / tokens / cost | {u['calls']} calls, {u['input_tokens']} in, {u['output_tokens']} out, ${u['cost_usd']:.4f} |")
    if pipe.get("incomplete"):
        out.append(f"| **Incomplete** | {pipe['incomplete']} |")
    if pipe["agent_failures"]:
        out.append(f"| Agent failures | {len(pipe['agent_failures'])} (listed at the end) |")
    out.append("")

    s = r["summary"]
    out += ["## Summary", ""]
    out += [s["executive_summary"] or "_No editor summary._", ""]
    for t in s["themes"]:
        out.append(f"- **{_md_escape(t['title'])}**: {', '.join(t['finding_ids'])}")
    if s["themes"]:
        out.append("")
    for issue in s["issues"]:
        out.append(f"> Editor check: {issue}")
    if s["issues"]:
        out.append("")

    sev_counts: dict[str, int] = {}
    for f in r["findings"]:
        sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1
    out += [f"## Findings ({len(r['findings'])})", "",
            ", ".join(f"{k}: {n}" for k, n in sev_counts.items()) or "None.", ""]
    for f in r["findings"]:
        out += _finding_md(f)

    if r["low_confidence"]:
        out += [f"## Low-confidence findings ({len(r['low_confidence'])})", ""]
        for f in r["low_confidence"]:
            out += _finding_md(f)
    if r["killed"]:
        out += [f"## Refuted by skeptics ({len(r['killed'])})", ""]
        for f in r["killed"]:
            out += _finding_md(f)
    if r["rejected"]:
        out += [f"## Rejected by the quote verifier ({len(r['rejected'])})", "", "| Agent | Kind | Title | Reason |", "|---|---|---|---|"]
        for x in r["rejected"]:
            out.append(f"| {x['source']} | {x['kind']} | {_md_escape(x['title'])[:90]} | {_md_escape('; '.join(x['reasons']))[:160]} |")
        out.append("")
    if pipe["agent_failures"]:
        out += ["## Agent failures", ""]
        for x in pipe["agent_failures"]:
            out.append(f"- {x.get('agent', '?')}: {x.get('error', '')}")
        out.append("")
    out += ["## Cited paragraphs", ""]
    for ref, p in r["paragraphs"].items():
        doc, pid = ref.split(":")
        out.append(f"<a id=\"{_anchor(doc, pid).lower()}\"></a>**{ref}** ({_md_escape(p['section'])})")
        out.append("")
        out.append(f"> {p['text']}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
