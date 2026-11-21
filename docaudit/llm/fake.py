"""FakeLLM: a scripted, deterministic test double for every agent role.

It is NOT a model and its output says nothing about model quality. It exists so
that every stage of the pipeline (fan-out, quote verification, re-attribution,
merge, coverage, gap reading, skeptic verdicts, recheck, editor checks, report)
runs offline and reproducibly on real documents.

Behaviour, all keyed on positions inside the agent's own input, so it does not
depend on call order or concurrency:

* section readers report one finding per changed alignment operation (diff) or
  per heuristic hit (audit), and deliberately inject faults on a fixed
  schedule: every 5th changed operation in a chunk is skipped (must surface in
  the coverage check), and every 4th finding carries a fault, cycling through
  a fabricated quote (must be rejected), a wrong paragraph id (must be
  re-attributed) and a case-changed quote (must match at the 'normalized'
  level);
* the gap reader reports half of the uncovered operations and dismisses the
  rest in its coverage note;
* skeptics refute changes that differ only by spelling or punctuation (with
  counter-evidence), weaken minor findings, refute deterministic numbering
  findings without counter-evidence (which code must treat as 'weakened'), and
  report uncovered operations next to their batch as 'missed';
* the editor writes a summary from the aggregated findings with one verbatim
  quote, which the report checks.
"""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher

from ..align import Alignment, Op
from ..ingest import Document, Paragraph
from ..sweeps import defined_terms, find_references, numbering_gaps
from ..textnorm import normalize_loose, tokens
from .base import LLMRequest, LLMResponse, Usage

EDITORIAL_VARIANTS = {
    "licence": "license", "licences": "licenses", "licenced": "licensed", "licencing": "licensing",
    "colour": "color", "organisation": "organization", "authorise": "authorize", "authorised": "authorized",
    "behaviour": "behavior", "favour": "favor", "programme": "program", "whilst": "while",
}
_SIGNAL_WORDS = {"not", "no", "may", "must", "shall", "should", "will", "never", "irrevocable", "revocable",
                 "exclusive", "only", "notify", "terminate", "within", "days", "years", "you", "licensor"}
_LABEL_RE = re.compile(r"^\(?[0-9a-z]{1,3}[.)]$")
_FABRICATED_TAIL = "shall be governed by the laws of the place where the Licensor resides"


def editorial_only(a_text: str, b_text: str) -> bool:
    ta = [EDITORIAL_VARIANTS.get(t, t) for t in tokens(a_text)]
    tb = [EDITORIAL_VARIANTS.get(t, t) for t in tokens(b_text)]
    return ta == tb


def _words(p: Paragraph) -> list[str]:
    return p.text.split(" ")


def _window(words: list[str], i1: int, i2: int, pad: int = 4) -> str:
    lo = max(0, i1 - pad)
    hi = min(len(words), max(i2, i1 + 1) + pad)
    while hi - lo < 3 and (lo > 0 or hi < len(words)):
        lo, hi = max(0, lo - 1), min(len(words), hi + 1)
    return " ".join(words[lo:hi])


def _absent_window(p: Paragraph, other: Document, size: int = 12) -> str:
    """A window of the paragraph that does not occur in the other document."""
    words = _words(p)
    other_loose = [normalize_loose(q.text) for q in other.paragraphs]
    for start in range(0, max(1, len(words) - size + 1), max(1, size // 2)):
        cand = " ".join(words[start:start + size])
        n = normalize_loose(cand)
        if n and not any(n in t for t in other_loose):
            return cand
    return p.text


def _severity(changed_words: list[str]) -> str:
    keys = {normalize_loose(w).strip(".,;:()") for w in changed_words}
    if any(any(c.isdigit() for c in k) for k in keys) or keys & _SIGNAL_WORDS:
        return "major"
    return "minor"


def _ev(doc: str, pid: str, quote: str) -> dict:
    return {"doc": doc, "para_id": pid, "quote": quote}


def change_finding(op: Op, docs: dict[str, Document]) -> dict | None:
    a, b = docs["A"], docs["B"]
    pa = a.para(op.a) if op.a else None
    pb = b.para(op.b) if op.b else None
    if op.op == "modified":
        wa, wb = _words(pa), _words(pb)
        ka = [normalize_loose(w) for w in wa]
        kb = [normalize_loose(w) for w in wb]
        codes = [c for c in SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes() if c[0] != "equal"]
        if not codes:
            return None
        # Skip a renumbered list label ("1." -> "4.") when the paragraph has a real edit too.
        real = [c for c in codes if not (c[1] == 0 and c[3] == 0 and all(_LABEL_RE.match(w) for w in wa[c[1]:c[2]] + wb[c[3]:c[4]]))]
        _, i1, i2, j1, j2 = (real or codes)[0]
        a_span = " ".join(wa[i1:i2]) or "(nothing)"
        b_span = " ".join(wb[j1:j2]) or "(nothing)"
        changed = wa[i1:i2] + wb[j1:j2]
        sev = _severity(changed)
        sec = b.section_of(pb.id).title
        if any(ch.isdigit() for ch in a_span + b_span):
            title = f"Value changed in {sec}: '{a_span}' became '{b_span}'"
        else:
            title = f"Wording changed in {sec}: '{' '.join(a_span.split()[:6])}' became '{' '.join(b_span.split()[:6])}'"
        more = f" {len(codes) - 1} further edit(s) in the same paragraph." if len(codes) > 1 else ""
        return {
            "kind": "changed",
            "title": title,
            "description": f"Version A reads \"{a_span}\" where version B reads \"{b_span}\".{more}",
            "severity": sev,
            "confidence": 0.7 if sev == "major" else 0.6,
            "evidence": [_ev("A", pa.id, _window(wa, i1, i2)), _ev("B", pb.id, _window(wb, j1, j2))],
        }
    if op.op == "inserted":
        words = pb.text.split()
        sev = _severity(words)
        return {
            "kind": "added",
            "title": f"New text in {b.section_of(pb.id).title}: {' '.join(words[:8])} ...",
            "description": "Version B contains this paragraph and version A has no counterpart for it.",
            "severity": sev,
            "confidence": 0.7 if sev == "major" else 0.6,
            "evidence": [_ev("B", pb.id, _absent_window(pb, a))],
        }
    if op.op == "deleted":
        words = pa.text.split()
        sev = _severity(words)
        return {
            "kind": "removed",
            "title": f"Text removed from {a.section_of(pa.id).title}: {' '.join(words[:8])} ...",
            "description": "Version A contains this paragraph and version B has no counterpart for it.",
            "severity": sev,
            "confidence": 0.7 if sev == "major" else 0.6,
            "evidence": [_ev("A", pa.id, _absent_window(pa, b))],
        }
    if op.op == "moved":
        return {
            "kind": "moved",
            "title": f"Paragraph moved from {a.section_of(pa.id).title} to {b.section_of(pb.id).title}",
            "description": "The same provision appears in a different place in version B.",
            "severity": "minor",
            "confidence": 0.65,
            "evidence": [_ev("A", pa.id, " ".join(pa.text.split()[:12])), _ev("B", pb.id, " ".join(pb.text.split()[:12]))],
        }
    return None


def _inject_fault(finding: dict, ordinal: int, docs: dict[str, Document]) -> dict:
    """Every 4th finding (ordinal 3, 7, 11, ...) gets a fault, cycling through three kinds."""
    if ordinal % 4 != 3:
        return finding
    r = (ordinal // 4) % 3
    ev = finding["evidence"][-1]
    doc = docs[ev["doc"]]
    if r == 0:
        ev["quote"] = " ".join(ev["quote"].split()[:3]) + " " + _FABRICATED_TAIL
    elif r == 1:
        p = doc.para(ev["para_id"])
        if p.index + 1 < len(doc.paragraphs):
            ev["para_id"] = doc.paragraphs[p.index + 1].id
    elif r == 2:
        q = ev["quote"]
        ev["quote"] = q.upper() if q[:1].islower() else q.lower()
    return finding


def _undefined_terms(doc: Document, pids: list[str]) -> list[dict]:
    terms = defined_terms(doc)
    heads = {t.split()[-1] for t in terms if len(t.split()) > 1}
    headings = " ".join(p.text for p in doc.paragraphs if p.kind == "heading")
    out = []
    seen = set()
    for pid in pids:
        p = doc.para(pid)
        if p.kind == "heading":
            continue
        for m in re.finditer(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+){1,2})\b", p.text):
            phrase = m.group(1)
            if phrase.split()[-1] not in heads or phrase in terms or phrase in seen:
                continue
            if any(phrase in t or phrase.endswith(t) for t in terms) or m.start() == 0 or phrase in headings:
                continue
            seen.add(phrase)
            out.append({
                "kind": "undefined_term",
                "title": f"'{phrase}' is used like a defined term but is never defined",
                "description": f"The capitalised phrase '{phrase}' reads like a defined term, but no definition exists.",
                "severity": "major",
                "confidence": 0.6,
                "evidence": [_ev(doc.key, pid, p.text[max(0, m.start() - 30): m.end() + 30].strip())],
            })
    return out


class FakeBackend:
    name = "fake"
    model = None

    def complete(self, req: LLMRequest) -> LLMResponse:
        handler = getattr(self, f"_{req.role}")
        data = handler(req.context)
        size_in = len(req.system) + len(req.prompt) + len(req.prefix or "")
        usage = Usage(input_tokens=size_in // 4, output_tokens=len(json.dumps(data)) // 4)
        return LLMResponse(data=data, usage=usage, model="fake", stop_reason="end_turn")

    # ------------------------------------------------------------ readers

    def _section_reader(self, ctx: dict) -> dict:
        docs, chunk = ctx["docs"], ctx["chunk"]
        findings, skipped = [], []
        if ctx["mode"] == "diff":
            al: Alignment = ctx["alignment"]
            changed = [al.ops[i] for i in chunk["ops"] if al.ops[i].op != "equal"]
            for n, op in enumerate(changed):
                if n % 5 == 4:
                    skipped.append(op.index)
                    continue
                f = change_finding(op, docs)
                if f:
                    findings.append(_inject_fault(f, len(findings), docs))
            note = f"Reviewed {len(chunk['ops'])} operations; did not get to ops {skipped}." if skipped else "Reviewed every operation."
            return {"findings": findings, "coverage_note": note}
        doc = docs["A"]
        pids = chunk["paras"]["A"]
        for r in find_references(doc):
            if r.para_id in pids and r.status in ("dangling", "missing_subitem"):
                findings.append({"kind": "broken_reference", "title": f"{r.text} points nowhere",
                                 "description": f"{r.detail}.", "severity": "major", "confidence": 0.7,
                                 "evidence": [_ev("A", r.para_id, r.text)]})
        findings += _undefined_terms(doc, pids)
        findings = [_inject_fault(f, i, docs) for i, f in enumerate(findings)]
        return {"findings": findings, "coverage_note": f"Reviewed {len(pids)} paragraphs."}

    def _gap_reader(self, ctx: dict) -> dict:
        docs, al = ctx["docs"], ctx["alignment"]
        findings, dismissed = [], []
        for idx in ctx["ops"]:
            if idx % 2 == 0:
                f = change_finding(al.ops[idx], docs)
                if f:
                    findings.append(f)
            else:
                dismissed.append(idx)
        return {"findings": findings, "coverage_note": f"Judged ops {dismissed} editorial." if dismissed else "All listed ops reported."}

    def _cross_reference_checker(self, ctx: dict) -> dict:
        docs = ctx["docs"]
        findings = []
        if ctx["mode"] == "diff":
            al: Alignment = ctx["alignment"]
            for op in al.ops:
                if op.op != "modified":
                    continue
                f = change_finding(op, docs)
                if f and f["title"].startswith("Value changed"):
                    f["title"] = "Cross-check: " + f["title"]
                    f["confidence"] = 0.6
                    findings.append(f)
            target = docs["B"]
        else:
            target = docs["A"]
            findings += _undefined_terms(target, [p.id for p in target.paragraphs])
        for g in numbering_gaps(target):
            findings.append({"kind": "omission", "title": f"List skips item {g['expected']}",
                             "description": "The numbering jumps, so an item may be missing.", "severity": "minor",
                             "confidence": 0.5,
                             "evidence": [_ev(target.key, g["after"].id, " ".join(g["after"].text.split()[:8]))]})
        return {"findings": findings, "coverage_note": "Checked numeric changes, list numbering and defined terms across the text."}

    # ------------------------------------------------------------ skeptic

    def _skeptic(self, ctx: dict) -> dict:
        docs, al, mode = ctx["docs"], ctx["alignment"], ctx["mode"]
        verdicts, missed = [], []
        a2op = al.op_of_para() if al else {}
        for f in ctx["findings"]:
            ev0 = f["evidence"][0]
            verdict = {"finding_id": f["id"], "verdict": "upheld", "reason": "Re-read the cited text; the finding holds.",
                       "suggested_severity": "keep", "counter_evidence": []}
            if mode == "diff" and f["kind"] in ("changed", "moved"):
                op = al.ops[a2op[(ev0["doc"], ev0["para_id"])]] if (ev0["doc"], ev0["para_id"]) in a2op else None
                if op and op.a and op.b and editorial_only(docs["A"].para(op.a).text, docs["B"].para(op.b).text):
                    verdict.update(verdict="refuted", suggested_severity="info",
                                   reason="Only spelling or punctuation differs between the versions; the meaning is unchanged.",
                                   counter_evidence=[{"doc": e["doc"], "para_id": e["para_id"], "quote": e["quote"]} for e in f["evidence"][:2]])
            if verdict["verdict"] == "upheld" and f["kind"] == "omission" and "sweep" in f["sources"]:
                verdict.update(verdict="refuted", reason="The numbering may be intentional.", suggested_severity="keep")
            elif verdict["verdict"] == "upheld" and f["severity"] == "minor":
                verdict.update(verdict="weakened", reason="Real, but the practical effect is limited.", suggested_severity="keep",
                               counter_evidence=[{"doc": ev0["doc"], "para_id": ev0["para_id"], "quote": ev0["quote"]}])
            verdicts.append(verdict)
        if al is not None and ctx.get("all_findings") is not None:
            cited = {(e["doc"], e["para_id"]) for g in ctx["all_findings"] for e in g["evidence"]}
            near = set()
            for f in ctx["findings"]:
                for e in f["evidence"]:
                    if (e["doc"], e["para_id"]) in a2op:
                        k = a2op[(e["doc"], e["para_id"])]
                        near.update(range(k - 2, k + 3))
            for op in al.changed_ops():
                if op.index not in near:
                    continue
                if (op.a and ("A", op.a) in cited) or (op.b and ("B", op.b) in cited):
                    continue
                g = change_finding(op, docs)
                if g:
                    missed.append(g)
        return {"verdicts": verdicts, "missed": missed}

    # ------------------------------------------------------------ editor

    def _editor(self, ctx: dict) -> dict:
        agg = ctx["aggregated"]
        main = agg["findings"]
        if not main:
            return {"executive_summary": "No finding survived verification and review.", "themes": [], "ordered_finding_ids": []}
        top = main[0]
        quote = top["evidence"][-1]["quote"]
        sev: dict[str, int] = {}
        for f in main:
            sev[f["severity"]] = sev.get(f["severity"], 0) + 1
        parts = ", ".join(f"{n} {s}" for s, n in sev.items())
        summary = (f"{len(main)} findings survived quote verification and the skeptic stage ({parts}). "
                   f"The first to read is {top['id']}: {top['title']}. Its evidence reads \"{quote}\". "
                   f"{len(agg['killed'])} findings were refuted by skeptics and {len(agg['low_confidence'])} are low-confidence.")
        themes: dict[str, list[str]] = {}
        for f in main:
            themes.setdefault(f["kind"], []).append(f["id"])
        return {
            "executive_summary": summary,
            "themes": [{"title": f"{k} ({len(v)})", "finding_ids": v} for k, v in themes.items()],
            "ordered_finding_ids": [f["id"] for f in main],
        }
