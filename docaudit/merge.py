"""Merge and de-duplicate accepted findings across agents.

Two findings are the same issue when all of these hold:

* same family: change kinds (added/removed/changed/moved) never merge with
  defect kinds (contradiction, broken_reference, ...), because "the clause was
  edited" and "the edit broke a reference" are different statements;
* they cite at least one common paragraph (after re-attribution);
* their quoted spans in that paragraph intersect, or their titles and
  descriptions share at least ``text_threshold`` of their content words
  (Jaccard).

Merged findings keep the union of evidence, the most severe severity, and a
noisy-OR of the member confidences: independent agents that report the same
quoted issue raise confidence, a single agent does not.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher

from .align import Alignment
from .ingest import Document
from .schemas import DIFF_KINDS, SEVERITIES
from .textnorm import normalize_loose, split_ellipsis
from .verify import VerifiedFinding

_STOP = set(
    "a an and are as at be by for from has have in is it its of on or that the this to was were will with "
    "not no b version text section paragraph clause".split()
)
SEV_RANK = {s: len(SEVERITIES) - i for i, s in enumerate(SEVERITIES)}  # critical=4 ... info=1


def family(kind: str) -> str:
    return "change" if kind in DIFF_KINDS else "defect"


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"\w+", normalize_loose(text)) if w not in _STOP and len(w) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _span(para_loose: str, quote: str) -> tuple[int, int] | None:
    """Character span of a quote inside its paragraph (loose forms); elided quotes span first to last segment."""
    segs = [normalize_loose(s) for s in split_ellipsis(quote)] or [normalize_loose(quote)]
    start = para_loose.find(segs[0])
    if start < 0:
        return None
    end = start + len(segs[0])
    for seg in segs[1:]:
        k = para_loose.find(seg, end)
        if k < 0:
            break
        end = k + len(seg)
    return start, end


def _quotes_overlap(q1: str, q2: str, para_text: str | None = None) -> bool:
    """Two quotes point at the same place: their spans in the paragraph intersect."""
    a, b = normalize_loose(q1), normalize_loose(q2)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    if para_text is not None:
        loose = normalize_loose(para_text)
        s1, s2 = _span(loose, q1), _span(loose, q2)
        if s1 and s2 and s1[0] < s2[1] and s2[0] < s1[1]:
            return True
    return SequenceMatcher(None, a, b, autojunk=False).ratio() >= 0.8


@dataclass
class MergedFinding:
    id: str
    kind: str
    title: str
    description: str
    severity: str
    confidence: float
    evidence: list[dict]
    sources: list[str]
    members: int
    position: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "sources": self.sources,
            "members": self.members,
            "position": self.position,
        }


def _cited(v: VerifiedFinding) -> set[tuple[str, str]]:
    return {(c.doc, c.found_para) for c in v.evidence if c.ok}


def same_issue(x: VerifiedFinding, y: VerifiedFinding, docs: dict[str, Document] | None = None,
               text_threshold: float = 0.35) -> bool:
    if family(x.kind) != family(y.kind):
        return False
    shared = _cited(x) & _cited(y)
    if not shared:
        return False
    for cx in x.evidence:
        for cy in y.evidence:
            if (cx.doc, cx.found_para) == (cy.doc, cy.found_para) and (cx.doc, cx.found_para) in shared:
                para = docs[cx.doc].para(cx.found_para).text if docs else None
                if _quotes_overlap(cx.quote, cy.quote, para):
                    return True
    wx = _content_words(x.title + " " + x.description)
    wy = _content_words(y.title + " " + y.description)
    return _jaccard(wx, wy) >= text_threshold


def noisy_or(confidences: list[float]) -> float:
    p = 1.0
    for c in confidences:
        p *= 1.0 - min(0.95, max(0.05, c))
    return round(min(0.99, 1.0 - p), 4)


def position_key(evidence: list[dict], docs: dict[str, Document], alignment: Alignment | None) -> list:
    if alignment is not None:
        a2op = alignment.op_of_para()
        ops = [a2op.get((e["doc"], e["para_id"]), 10**6) for e in evidence]
        return [min(ops) if ops else 10**6]
    idx = [docs[e["doc"]].para(e["para_id"]).index for e in evidence]
    return [min(idx) if idx else 10**6]


def _cluster(findings: list[VerifiedFinding], docs: dict[str, Document]) -> list[list[int]]:
    parent = list(range(len(findings)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(findings)):
        for j in range(i + 1, len(findings)):
            if find(i) != find(j) and same_issue(findings[i], findings[j], docs):
                parent[find(j)] = find(i)
    groups: dict[int, list[int]] = {}
    for i in range(len(findings)):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def build_merged(members: list[VerifiedFinding], docs: dict[str, Document], alignment: Alignment | None) -> MergedFinding:
    ranked = sorted(members, key=lambda v: (-v.confidence, v.source, v.title))
    rep = ranked[0]
    kinds = Counter(v.kind for v in members)
    top = max(kinds.values())
    kind = rep.kind if kinds[rep.kind] == top else sorted(k for k, n in kinds.items() if n == top)[0]
    severity = max((v.severity for v in members), key=lambda s: SEV_RANK[s])
    seen = set()
    evidence = []
    for v in ranked:
        for c in v.evidence:
            key = (c.doc, c.found_para, normalize_loose(c.quote))
            if key in seen:
                continue
            seen.add(key)
            evidence.append({"doc": c.doc, "para_id": c.found_para, "quote": c.quote.strip(), "match": c.match, "relocated": c.relocated})
    evidence.sort(key=lambda e: (e["doc"], docs[e["doc"]].para(e["para_id"]).index))
    return MergedFinding(
        id="",
        kind=kind,
        title=rep.title,
        description=rep.description,
        severity=severity,
        confidence=noisy_or([v.confidence for v in members]),
        evidence=evidence,
        sources=sorted({v.source for v in members}),
        members=len(members),
        position=position_key(evidence, docs, alignment),
    )


def merge_findings(accepted: list[VerifiedFinding], docs: dict[str, Document], alignment: Alignment | None,
                   id_start: int = 1) -> list[MergedFinding]:
    merged = [build_merged([accepted[i] for i in g], docs, alignment) for g in _cluster(accepted, docs)]
    merged.sort(key=lambda m: (m.position, m.kind, m.title))
    for n, m in enumerate(merged, start=id_start):
        m.id = f"F{n:03d}"
    return merged


def coverage(alignment: Alignment, findings: list[dict]) -> dict:
    cited = {(e["doc"], e["para_id"]) for f in findings for e in f["evidence"]}
    changed = alignment.changed_ops()
    uncovered = [o.index for o in changed if not ((o.a and ("A", o.a) in cited) or (o.b and ("B", o.b) in cited))]
    n = len(changed)
    return {
        "changed_ops": n,
        "covered": n - len(uncovered),
        "ratio": round((n - len(uncovered)) / n, 4) if n else 1.0,
        "uncovered": uncovered,
    }
