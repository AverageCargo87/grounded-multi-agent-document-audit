"""Deterministic sweeps: things code can check exactly, before any agent runs.

* Cross-references ("Section 6(b)", "Sections 1, 5, and 8") are resolved
  against the document's own section numbers and list-item labels.
* List numbering is checked for gaps (1, 2, 4) per nesting level.
* Defined terms and numeric expressions are indexed for the cross-reference
  checker agent.

Sweep findings use the same shape as agent findings and go through the same
verifier, merge and skeptic stages, so a dangling reference that an agent also
reports is merged rather than double counted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .ingest import Document, Paragraph

_REF_RE = re.compile(
    r"\b([Ss]ections?)\s+"
    r"(\d+(?:\s*\([A-Za-z0-9]{1,4}\))*(?:\s*-\s*\([A-Za-z0-9]{1,4}\))?"
    r"(?:(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or)\s+)\d+(?:\s*\([A-Za-z0-9]{1,4}\))*)*)"
)
_REF_ITEM_RE = re.compile(r"(\d+)((?:\s*\([A-Za-z0-9]{1,4}\))*)")
_SUB_RE = re.compile(r"\(([A-Za-z0-9]{1,4})\)")
_LABEL_RE = re.compile(r"^\(?([a-z]{1,4}|\d{1,3}|[A-Z])[.)]\s+")
_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}
_DEF_RE = re.compile(
    r"^(?:\(?[a-z0-9]{1,4}[.)]\s+)?"
    r"([A-Z][\w']*(?:\s+(?:and\s+)?[A-Z][\w'()]*){0,5})\s+(?:means|shall mean|refers to)\b"
)
_QUOTED_DEF_RE = re.compile(
    r"[\"\u201c]([^\"\u201d]{1,60})[\"\u201d][^.\"\u201c]{0,60}?\b(?:also\s+)?(?:means|refers to|shall mean)\b"
)
_PAREN_DEF_RE = re.compile(r"\(\s*(?:the\s+)?[\"\u201c]([^\"\u201d]{1,60})[\"\u201d]\s*\)")
_NUMERIC_RE = re.compile(
    r"\b(\d+(?:[.,]\d+)?)\s*(%|percent|per cent|days?|weeks?|months?|years?|hours?)\b",
    re.IGNORECASE,
)


@dataclass
class Reference:
    para_id: str
    text: str  # verbatim span from the paragraph
    section: str
    path: list[str]
    status: str  # ok | dangling | missing_subitem | unresolved_subpath
    detail: str


def _roman_value(s: str) -> int | None:
    s = s.lower()
    if not s or any(c not in _ROMAN for c in s):
        return None
    total, prev = 0, 0
    for c in reversed(s):
        v = _ROMAN[c]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


def _label_of(p: Paragraph) -> tuple[str, int] | None:
    """(label, content column) for a list item paragraph."""
    if p.kind != "list_item":
        return None
    m = _LABEL_RE.match(p.text)
    if not m:
        return None
    return m.group(1), p.indent + m.end()


def _section_items(doc: Document) -> dict[str, list[tuple[Paragraph, str, int]]]:
    out: dict[str, list[tuple[Paragraph, str, int]]] = {}
    for sec in doc.sections:
        items = []
        for pid in sec.para_ids:
            p = doc.para(pid)
            lab = _label_of(p)
            # A numbered paragraph that opened an implicit section is the section, not an item.
            if lab and not (sec.number is not None and pid == sec.para_ids[0] and lab[0] == sec.number):
                items.append((p, lab[0], lab[1]))
        out[sec.key] = items
    return out


def _resolve_path(items: list[tuple[Paragraph, str, int]], path: list[str]) -> tuple[int, Paragraph | None]:
    """Walk list items by nesting (content column). Returns (levels resolved, target)."""
    candidates = items
    depth = 0
    target = None
    for comp in path:
        if not candidates:
            break
        top_col = min(c for _, _, c in candidates)
        found_idx = None
        for k, (p, lab, col) in enumerate(candidates):
            if col == top_col and lab.lower() == comp.lower():
                found_idx = k
                break
        if found_idx is None:
            break
        depth += 1
        target, _, col = candidates[found_idx]
        children = []
        for p, lab, c in candidates[found_idx + 1 :]:
            if c <= col:
                break
            children.append((p, lab, c))
        candidates = children
    return depth, target


def find_references(doc: Document) -> list[Reference]:
    numbers = {s.number for s in doc.sections if s.number is not None}
    sec_by_number: dict[str, str] = {}
    for s in doc.sections:
        if s.number is not None and s.number not in sec_by_number:
            sec_by_number[s.number] = s.key
    items_by_sec = _section_items(doc)
    refs: list[Reference] = []
    for p in doc.paragraphs:
        if p.kind == "heading":
            continue
        for m in _REF_RE.finditer(p.text):
            group = m.group(2)
            for im in _REF_ITEM_RE.finditer(group):
                num = im.group(1)
                path = _SUB_RE.findall(im.group(2) or "")
                if num not in numbers:
                    refs.append(Reference(p.id, m.group(0), num, path, "dangling", f"no Section {num} in this document"))
                    continue
                items = items_by_sec.get(sec_by_number[num], [])
                if not path:
                    refs.append(Reference(p.id, m.group(0), num, path, "ok", ""))
                    continue
                depth, _ = _resolve_path(items, path)
                if depth == len(path):
                    status, detail = "ok", ""
                elif depth == 0 and items:
                    status, detail = "missing_subitem", f"Section {num} has no item ({path[0]})"
                else:
                    status, detail = "unresolved_subpath", f"resolved {depth} of {len(path)} levels"
                refs.append(Reference(p.id, m.group(0), num, path, status, detail))
    return refs


def _next_label(prev: str, kind: str) -> str | None:
    if kind == "digit":
        return str(int(prev) + 1)
    if kind == "roman":
        v = _roman_value(prev)
        table = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv"]
        return table[v] if v is not None and v < len(table) else None
    if kind in ("lower", "upper") and len(prev) == 1:
        return chr(ord(prev) + 1)
    return None


def _label_kind(label: str, prev_kind: str | None) -> str:
    if label.isdigit():
        return "digit"
    if label.isupper():
        return "upper"
    if prev_kind == "roman" and _roman_value(label) is not None:
        return "roman"
    if prev_kind is None and label in ("i",):
        return "roman"
    if len(label) > 1 and _roman_value(label) is not None:
        return "roman"
    return "lower"


def numbering_gaps(doc: Document) -> list[dict]:
    """List items whose label skips one or more expected labels at the same level."""
    gaps = []
    items_by_sec = _section_items(doc)
    for sec in doc.sections:
        state: dict[int, tuple[str, str, Paragraph]] = {}
        for p, label, col in items_by_sec.get(sec.key, []):
            for c in [c for c in state if c > col]:
                del state[c]
            prev = state.get(col)
            kind = _label_kind(label, prev[1] if prev else None)
            if prev and prev[1] == kind:
                expected = _next_label(prev[0], kind)
                if expected is not None and label.lower() != expected.lower():
                    gaps.append({"section": sec.key, "before": prev[2], "after": p, "expected": expected, "found": label})
            state[col] = (label, kind, p)
    # Top-level section numbers.
    nums = [(s, int(s.number)) for s in doc.sections if s.number is not None and s.number.isdigit()]
    for (s1, n1), (s2, n2) in zip(nums, nums[1:]):
        if n2 > n1 + 1:
            p1, p2 = doc.para(s1.para_ids[0]), doc.para(s2.para_ids[0])
            gaps.append({"section": s2.key, "before": p1, "after": p2, "expected": str(n1 + 1), "found": str(n2)})
    return gaps


def defined_terms(doc: Document) -> dict[str, str]:
    terms: dict[str, str] = {}
    for p in doc.paragraphs:
        m = _DEF_RE.match(p.text)
        if m:
            terms.setdefault(m.group(1).strip(), p.id)
        for qm in _QUOTED_DEF_RE.finditer(p.text):
            terms.setdefault(qm.group(1).strip(), p.id)
        for pm in _PAREN_DEF_RE.finditer(p.text):
            terms.setdefault(pm.group(1).strip(), p.id)
    return terms


def numeric_facts(doc: Document) -> list[dict]:
    facts = []
    for p in doc.paragraphs:
        for m in _NUMERIC_RE.finditer(p.text):
            start = max(0, m.start() - 40)
            facts.append({"para_id": p.id, "value": m.group(0), "context": p.text[start : m.end() + 40]})
    return facts


def _first_words(text: str, n: int = 8) -> str:
    return " ".join(text.split()[:n])


def sweep_findings(doc: Document, baseline_doc: Document | None = None) -> list[dict]:
    """Findings that code can establish on its own.

    With ``baseline_doc`` (diff mode) only problems that the baseline does not
    already have are reported, so a dangling reference that existed in A is not
    blamed on the edit.
    """
    findings: list[dict] = []
    old_refs = set()
    if baseline_doc is not None:
        old_refs = {r.text for r in find_references(baseline_doc) if r.status in ("dangling", "missing_subitem")}
    for r in find_references(doc):
        if r.status not in ("dangling", "missing_subitem") or r.text in old_refs:
            continue
        findings.append({
            "kind": "broken_reference",
            "title": f"Cross-reference to a non-existent target: {r.text}",
            "description": f"The text refers to {r.text}, but {r.detail}.",
            "severity": "major",
            "confidence": 0.9,
            "evidence": [{"doc": doc.key, "para_id": r.para_id, "quote": r.text}],
        })
    old_gaps = set()
    if baseline_doc is not None:
        old_gaps = {(_first_words(g["after"].text), g["expected"]) for g in numbering_gaps(baseline_doc)}
    for g in numbering_gaps(doc):
        if (_first_words(g["after"].text), g["expected"]) in old_gaps:
            continue
        findings.append({
            "kind": "omission",
            "title": f"Numbering gap: item {g['expected']} is missing",
            "description": (
                f"Item {g['found']} follows the item before it, but {g['expected']} was expected; "
                "an item may have been deleted or the list renumbered incompletely."
            ),
            "severity": "minor",
            "confidence": 0.8,
            "evidence": [
                {"doc": doc.key, "para_id": g["before"].id, "quote": _first_words(g["before"].text)},
                {"doc": doc.key, "para_id": g["after"].id, "quote": _first_words(g["after"].text)},
            ],
        })
    return findings
