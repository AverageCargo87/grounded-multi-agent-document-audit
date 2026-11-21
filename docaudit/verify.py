"""The quote verifier: no finding survives on an agent's word alone.

Every evidence item an agent emits is ``{doc, para_id, quote}``. Code checks
that the quote really is in that paragraph, at one of three match levels:

* exact       the quote is a substring of the paragraph after whitespace collapse
* normalized  it matches after typography folding, de-hyphenation and case folding
* elided      "..." joins verbatim segments (two words or more each), in order

A quote found in a different paragraph of the same document is re-attributed
(``relocated``) rather than rejected: wrong paragraph ids are a common, benign
model error. A quote found nowhere, or only in the other document, rejects the
whole finding. In diff mode the claim itself is also checked: text quoted as
"added" must not occur anywhere in A, text quoted as "removed" must not occur
anywhere in B, and a "changed" claim must quote something that differs.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher

from .ingest import Document
from .schemas import FINDING, KINDS_BY_MODE, SEVERITIES, validate
from .textnorm import collapse_ws, normalize_loose, split_ellipsis, word_count

_WRAPPING_QUOTES = {('"', '"'), ("'", "'"), ("\u201c", "\u201d"), ("\u2018", "\u2019"), ("\u00ab", "\u00bb")}


@dataclass
class EvidenceCheck:
    doc: str
    para_id: str
    quote: str
    ok: bool
    match: str  # exact | normalized | elided | none
    found_para: str | None
    relocated: bool
    reason: str = ""
    common: float = 0.0


@dataclass
class VerifiedFinding:
    source: str
    kind: str
    title: str
    description: str
    severity: str
    confidence: float
    evidence: list[EvidenceCheck]
    status: str  # accepted | rejected
    reasons: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    code: str = ""  # first rejection code, empty when accepted

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


class DocIndex:
    """Caches the whitespace-collapsed and loose forms of every paragraph."""

    def __init__(self, docs: dict[str, Document]) -> None:
        self.docs = docs
        self.light: dict[tuple[str, str], str] = {}
        self.loose: dict[tuple[str, str], str] = {}
        for key, doc in docs.items():
            for p in doc.paragraphs:
                self.light[(key, p.id)] = collapse_ws(p.text)
                self.loose[(key, p.id)] = normalize_loose(p.text)

    def match_level(self, doc_key: str, pid: str, quote: str) -> str | None:
        light = self.light.get((doc_key, pid))
        if light is None:
            return None
        q_light = collapse_ws(quote)
        if q_light and q_light in light:
            return "exact"
        loose = self.loose[(doc_key, pid)]
        q_loose = normalize_loose(quote)
        if q_loose and q_loose in loose:
            return "normalized"
        segs = split_ellipsis(quote)
        if len(segs) >= 2 and all(word_count(s) >= 2 for s in segs):
            pos = 0
            for s in segs:
                ns = normalize_loose(s)
                k = loose.find(ns, pos)
                if k < 0:
                    return None
                pos = k + len(ns)
            return "elided"
        return None

    def locate(self, doc_key: str, quote: str) -> list[tuple[str, str]]:
        doc = self.docs.get(doc_key)
        if doc is None:
            return []
        hits = []
        for p in doc.paragraphs:
            lvl = self.match_level(doc_key, p.id, quote)
            if lvl:
                hits.append((p.id, lvl))
        return hits

    def occurs(self, doc_key: str, quote: str) -> str | None:
        """Paragraph id where the quote (or its longest elided segment) occurs, loosely."""
        segs = split_ellipsis(quote) or [quote]
        probe = normalize_loose(max(segs, key=len))
        if not probe:
            return None
        doc = self.docs.get(doc_key)
        if doc is None:
            return None
        for p in doc.paragraphs:
            if probe in self.loose[(doc_key, p.id)]:
                return p.id
        return None


def _strip_wrapping(quote: str) -> str:
    q = quote.strip()
    if len(q) >= 2 and (q[0], q[-1]) in _WRAPPING_QUOTES:
        q = q[1:-1].strip()
    return q


def _common_fraction(quote: str, text: str) -> float:
    q, t = normalize_loose(quote), normalize_loose(text)
    if not q or not t:
        return 0.0
    m = SequenceMatcher(None, q, t, autojunk=False).find_longest_match(0, len(q), 0, len(t))
    return round(m.size / len(q), 3)


def check_quote(index: DocIndex, doc_key: str, para_id: str, quote: str, min_chars: int = 6) -> EvidenceCheck:
    q = _strip_wrapping(quote or "")
    if doc_key not in index.docs:
        return EvidenceCheck(doc_key, para_id, quote, False, "none", None, False, f"unknown_document '{doc_key}'")
    if len(normalize_loose(q)) < min_chars:
        return EvidenceCheck(doc_key, para_id, quote, False, "none", None, False, "quote_too_short")
    lvl = index.match_level(doc_key, para_id, q)
    if lvl:
        return EvidenceCheck(doc_key, para_id, quote, True, lvl, para_id, False)
    hits = index.locate(doc_key, q)
    if hits:
        doc = index.docs[doc_key]
        cited = doc.para(para_id)
        if cited is not None:
            hits.sort(key=lambda h: (abs(doc.para(h[0]).index - cited.index), doc.para(h[0]).index))
        pid, lvl = hits[0]
        return EvidenceCheck(doc_key, para_id, quote, True, lvl, pid, True, f"relocated from {para_id} to {pid}")
    for other in index.docs:
        if other != doc_key and index.locate(other, q):
            return EvidenceCheck(doc_key, para_id, quote, False, "none", None, False, f"quote_in_other_doc_only ({other})")
    cited = index.docs[doc_key].para(para_id)
    common = _common_fraction(q, cited.text) if cited else 0.0
    reason = "quote_not_found" if cited else f"quote_not_found (unknown paragraph {para_id})"
    return EvidenceCheck(doc_key, para_id, quote, False, "none", None, False, reason, common)


def verify_finding(raw: dict, source: str, mode: str, index: DocIndex) -> VerifiedFinding:
    def rejected(reason: str, evidence: list[EvidenceCheck] | None = None) -> VerifiedFinding:
        return VerifiedFinding(
            source=source,
            kind=str(raw.get("kind", "")) if isinstance(raw, dict) else "",
            title=str(raw.get("title", "")) if isinstance(raw, dict) else "",
            description=str(raw.get("description", "")) if isinstance(raw, dict) else "",
            severity=str(raw.get("severity", "")) if isinstance(raw, dict) else "",
            confidence=0.0,
            evidence=evidence or [],
            status="rejected",
            reasons=[reason],
            code=re.match(r"[A-Za-z_]+", reason).group(0),
        )

    errors = validate(raw, FINDING)
    if errors:
        return rejected("schema_invalid: " + "; ".join(errors[:3]))
    kind = raw["kind"]
    if kind not in KINDS_BY_MODE[mode]:
        return rejected(f"kind_not_allowed_in_{mode}_mode: {kind}")
    notes = []
    conf = float(raw["confidence"])
    if not 0.0 <= conf <= 1.0:
        notes.append(f"confidence {conf} clamped")
        conf = min(1.0, max(0.0, conf))
    if raw["severity"] not in SEVERITIES:
        return rejected("bad_severity")
    if not raw["evidence"]:
        return rejected("no_evidence")
    allowed_docs = set(index.docs)
    checks = []
    for e in raw["evidence"]:
        if e["doc"] not in allowed_docs:
            return rejected(f"unknown_document: evidence cites '{e['doc']}', which is not part of this run")
        checks.append(check_quote(index, e["doc"], e["para_id"], e["quote"]))
    failed = [c for c in checks if not c.ok]
    if failed:
        reasons = [f"{c.doc}:{c.para_id} {c.reason}" + (f" (longest common run {c.common:.0%} of quote)" if c.common else "") for c in failed]
        vf = rejected(failed[0].reason, checks)
        vf.reasons = reasons
        return vf

    if mode == "diff":
        a_quotes = [c for c in checks if c.doc == "A"]
        b_quotes = [c for c in checks if c.doc == "B"]
        if kind == "added":
            if not b_quotes:
                return rejected("added_needs_B_evidence", checks)
            for c in b_quotes:
                hit = index.occurs("A", _strip_wrapping(c.quote))
                if hit:
                    return rejected(f"added_text_present_in_A (A:{hit})", checks)
        elif kind == "removed":
            if not a_quotes:
                return rejected("removed_needs_A_evidence", checks)
            for c in a_quotes:
                hit = index.occurs("B", _strip_wrapping(c.quote))
                if hit:
                    return rejected(f"removed_text_present_in_B (B:{hit})", checks)
        elif kind in ("changed", "moved"):
            if not a_quotes or not b_quotes:
                return rejected(f"{kind}_needs_both_sides", checks)
            if kind == "changed":
                a_in_b = all(index.occurs("B", _strip_wrapping(c.quote)) for c in a_quotes)
                b_in_a = all(index.occurs("A", _strip_wrapping(c.quote)) for c in b_quotes)
                if a_in_b and b_in_a:
                    return rejected("changed_without_difference: every quote occurs in both versions", checks)

    for c in checks:
        if c.relocated:
            notes.append(c.reason)
    return VerifiedFinding(
        source=source,
        kind=kind,
        title=raw["title"].strip(),
        description=raw["description"].strip(),
        severity=raw["severity"],
        confidence=conf,
        evidence=checks,
        status="accepted",
        notes=notes,
    )


def verification_stats(verified: list[VerifiedFinding]) -> dict:
    agent = [v for v in verified if not v.source.startswith("sweep")]
    rejected = [v for v in agent if v.status == "rejected"]
    reasons: dict[str, int] = {}
    for v in rejected:
        reasons[v.code] = reasons.get(v.code, 0) + 1
    levels: dict[str, int] = {}
    relocated = 0
    for v in agent:
        if v.status != "accepted":
            continue
        for c in v.evidence:
            levels[c.match] = levels.get(c.match, 0) + 1
            relocated += int(c.relocated)
    n = len(agent)
    return {
        "agent_findings": n,
        "accepted": n - len(rejected),
        "rejected": len(rejected),
        "rejection_rate": round(len(rejected) / n, 4) if n else 0.0,
        "rejection_reasons": dict(sorted(reasons.items())),
        "evidence_match_levels": dict(sorted(levels.items())),
        "evidence_relocated": relocated,
        "sweep_findings": len(verified) - n,
    }
