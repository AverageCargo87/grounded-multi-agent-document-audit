"""Evaluation harness: score any run directory against a ground-truth file.

Ground truth (``examples/planted/ground_truth.json``) lists planted changes and
defects. Each item names verbatim anchors that the scorer resolves to
paragraph ids at scoring time, so the truth file does not depend on the id
scheme. A finding matches an item when it cites at least one of the item's
paragraphs.

Metrics:

* recall: substantive items matched by at least one surviving finding (any
  severity; findings killed by skeptics do not count). In audit mode the
  finding's kind must also be one of the item's ``audit_kinds``;
* precision: among surviving findings of severity minor or higher, the share
  that match a substantive item. Findings that match only an item marked
  ``ignore`` are left out; findings that match nothing, or only an editorial
  (non-substantive) item, count against precision. ``info`` findings are
  treated as editorial notes and excluded from precision;
* skeptic false kills: substantive items whose only matching findings were
  killed by skeptics;
* quote verifier rejection rate: taken from the run's own verification log.

The deterministic baseline (``baseline``) needs no model: in diff mode every
changed alignment operation becomes a finding; in audit mode the
deterministic sweeps are the findings.
"""

from __future__ import annotations

import json
from pathlib import Path

from .ingest import Document
from .runstore import Run
from .textnorm import normalize_loose

KIND_BY_OP = {"modified": "changed", "inserted": "added", "deleted": "removed", "moved": "moved"}


def baseline(run_dir: str | Path) -> dict:
    run = Run(run_dir)
    docs = run.docs
    findings = []
    if run.mode == "diff":
        for op in run.alignment.changed_ops():
            ev = []
            if op.a:
                ev.append({"doc": "A", "para_id": op.a, "quote": " ".join(docs["A"].para(op.a).text.split()[:20])})
            if op.b:
                ev.append({"doc": "B", "para_id": op.b, "quote": " ".join(docs["B"].para(op.b).text.split()[:20])})
            findings.append({"id": f"X{op.index:03d}", "kind": KIND_BY_OP[op.op], "title": f"{op.op} paragraph (op {op.index})",
                             "severity": "minor", "confidence": 0.5, "evidence": ev})
        source = "every changed alignment operation"
    else:
        for n, f in enumerate(run.read_json("sweeps.json")["findings"], start=1):
            findings.append({"id": f"X{n:03d}", **f})
        source = "deterministic sweeps (cross-references, numbering)"
    out = {"source": source, "findings": findings}
    run.write_json("baseline.json", out)
    return {"stage": "baseline", "findings": len(findings), "source": source}


def resolve_anchor(doc: Document, anchor: str) -> str:
    probe = normalize_loose(anchor)
    hits = [p.id for p in doc.paragraphs if probe in normalize_loose(p.text)]
    if len(hits) != 1:
        raise ValueError(f"anchor {anchor!r} matches {len(hits)} paragraphs in {doc.source}; it must match exactly one")
    return hits[0]


def _item_paras(item: dict, mode: str, docs: dict[str, Document]) -> set[tuple[str, str]]:
    paras = set()
    if mode == "diff":
        for a in item.get("anchors_a", []):
            paras.add(("A", resolve_anchor(docs["A"], a)))
        for b in item.get("anchors_b", []):
            paras.add(("B", resolve_anchor(docs["B"], b)))
    else:
        for b in item.get("audit_anchors", []):
            paras.add(("A", resolve_anchor(docs["A"], b)))
    return paras


def score(run_dir: str | Path, truth_path: str | Path, source: str = "final") -> dict:
    run = Run(run_dir)
    mode = run.mode
    truth = json.loads(Path(truth_path).read_text(encoding="utf-8"))
    items = [it for it in truth["items"] if mode in it["modes"]]
    docs = run.docs
    paras = {it["id"]: _item_paras(it, mode, docs) for it in items}
    if source == "baseline":
        data = run.read_json("baseline.json")
        surviving, killed, verifier = data["findings"], [], None
    else:
        rep = run.read_json("report.json")
        surviving = rep["findings"] + rep["low_confidence"]
        killed = rep["killed"]
        verifier = rep["pipeline"]["verification"]

    def matches(f: dict) -> list[dict]:
        cited = {(e["doc"], e["para_id"]) for e in f["evidence"]}
        out = []
        for it in items:
            if not cited & paras[it["id"]]:
                continue
            if mode == "audit" and it.get("audit_kinds") and f["kind"] not in it["audit_kinds"]:
                continue  # right paragraph, wrong kind of defect
            out.append(it)
        return out

    found: set[str] = set()
    correct = wrong = ignored = info = 0
    editorial_flagged: set[str] = set()
    false_positives = []
    for f in surviving:
        m = matches(f)
        for it in m:
            if it["substantive"]:
                found.add(it["id"])
        if f["severity"] == "info":
            info += 1
            continue
        if any(it["substantive"] for it in m):
            correct += 1
        elif m and all(it.get("ignore") for it in m):
            ignored += 1
        else:
            wrong += 1
            editorial_flagged.update(it["id"] for it in m if not it["substantive"] and not it.get("ignore"))
            false_positives.append({"id": f.get("id"), "title": f.get("title"), "matched": [it["id"] for it in m]})
    substantive = [it for it in items if it["substantive"]]
    killed_items = set()
    for f in killed:
        for it in matches(f):
            if it["substantive"] and it["id"] not in found:
                killed_items.add(it["id"])
    by_cat: dict[str, list[int]] = {}
    for it in substantive:
        c = by_cat.setdefault(it["category"], [0, 0])
        c[1] += 1
        c[0] += int(it["id"] in found)
    reportable = correct + wrong
    recall = len(found) / len(substantive) if substantive else 0.0
    precision = correct / reportable if reportable else 0.0
    return {
        "run": run.plan["label"],
        "mode": mode,
        "source": source,
        "truth": Path(truth_path).as_posix() if not Path(truth_path).is_absolute() else Path(truth_path).name,
        "substantive_items": len(substantive),
        "found": sorted(found),
        "missed": sorted(it["id"] for it in substantive if it["id"] not in found),
        "recall": round(recall, 4),
        "precision": round(precision, 4),
        "f1": round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0.0,
        "findings_scored": reportable,
        "findings_correct": correct,
        "findings_wrong": wrong,
        "findings_info_excluded": info,
        "findings_on_ignored_items": ignored,
        "editorial_items_flagged": sorted(editorial_flagged),
        "false_positives": false_positives,
        "skeptic_false_kills": sorted(killed_items),
        "recall_by_category": {k: f"{v[0]}/{v[1]}" for k, v in sorted(by_cat.items())},
        "quote_verifier": None if verifier is None else {
            "agent_findings": verifier["agent_findings"],
            "rejected": verifier["rejected"],
            "rejection_rate": verifier["rejection_rate"],
            "rejection_reasons": verifier["rejection_reasons"],
        },
    }
