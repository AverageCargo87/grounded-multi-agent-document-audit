"""Paragraph and section alignment between version A and version B.

Algorithm (deterministic, no LLM):

1. Paragraphs whose fingerprints are unique in both versions are anchor
   candidates; the longest increasing subsequence of those pairs (by position)
   becomes the anchor set, so reordered duplicates cannot cross.
2. Between consecutive anchors a monotone dynamic programme (Needleman-Wunsch
   without gap penalties) pairs paragraphs, maximising the sum of
   ``similarity - min_sim`` over the pairs it keeps.
3. Leftover A paragraphs and B paragraphs that are near-identical
   (``similarity >= move_sim``) are paired as moves.
4. Everything else is an insertion (B only) or a deletion (A only).

Similarity is ``difflib.SequenceMatcher.ratio`` over word tokens of the
loose-normalised text, behind a cheap token-set Jaccard prefilter.
"""

from __future__ import annotations

from bisect import bisect_left
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher

from .ingest import Document
from .textnorm import tokens

EQUAL, MODIFIED, INSERTED, DELETED, MOVED = "equal", "modified", "inserted", "deleted", "moved"


@dataclass
class Op:
    index: int
    op: str
    a: str | None
    b: str | None
    sim: float


@dataclass
class Alignment:
    ops: list[Op]
    section_pairs: list[dict] = field(default_factory=list)

    def stats(self) -> dict:
        c = Counter(o.op for o in self.ops)
        return {k: c.get(k, 0) for k in (EQUAL, MODIFIED, INSERTED, DELETED, MOVED)}

    def changed_ops(self) -> list[Op]:
        return [o for o in self.ops if o.op != EQUAL]

    def to_dict(self) -> dict:
        return {"ops": [asdict(o) for o in self.ops], "section_pairs": self.section_pairs, "stats": self.stats()}

    @classmethod
    def from_dict(cls, data: dict) -> "Alignment":
        return cls(ops=[Op(**o) for o in data["ops"]], section_pairs=data.get("section_pairs", []))

    def op_of_para(self) -> dict[tuple[str, str], int]:
        out: dict[tuple[str, str], int] = {}
        for o in self.ops:
            if o.a:
                out[("A", o.a)] = o.index
            if o.b:
                out[("B", o.b)] = o.index
        return out


class _Sim:
    def __init__(self, a: Document, b: Document, jaccard_floor: float = 0.15) -> None:
        self.ta = [tokens(p.text) for p in a.paragraphs]
        self.tb = [tokens(p.text) for p in b.paragraphs]
        self.sa = [set(t) for t in self.ta]
        self.sb = [set(t) for t in self.tb]
        self.fa = [p.fingerprint for p in a.paragraphs]
        self.fb = [p.fingerprint for p in b.paragraphs]
        self.floor = jaccard_floor
        self.cache: dict[tuple[int, int], float] = {}

    def __call__(self, i: int, j: int) -> float:
        key = (i, j)
        if key in self.cache:
            return self.cache[key]
        if self.fa[i] == self.fb[j]:
            s = 1.0
        else:
            sa, sb = self.sa[i], self.sb[j]
            union = len(sa | sb)
            jac = len(sa & sb) / union if union else 0.0
            if jac < self.floor:
                s = 0.0
            else:
                s = SequenceMatcher(None, self.ta[i], self.tb[j], autojunk=False).ratio()
                s = min(s, 0.999)  # 1.0 is reserved for identical fingerprints
        self.cache[key] = s
        return s


def _lis(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Longest strictly increasing subsequence in the second coordinate."""
    pairs = sorted(pairs)
    tails: list[int] = []
    tails_idx: list[int] = []
    prev = [-1] * len(pairs)
    for k, (_, j) in enumerate(pairs):
        pos = bisect_left(tails, j)
        if pos == len(tails):
            tails.append(j)
            tails_idx.append(k)
        else:
            tails[pos] = j
            tails_idx[pos] = k
        prev[k] = tails_idx[pos - 1] if pos > 0 else -1
    out = []
    k = tails_idx[-1] if tails_idx else -1
    while k != -1:
        out.append(pairs[k])
        k = prev[k]
    return out[::-1]


def _dp(i0: int, i1: int, j0: int, j1: int, sim: _Sim, min_sim: float) -> list[tuple[int, int]]:
    n, m = i1 - i0, j1 - j0
    if n <= 0 or m <= 0:
        return []
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]  # 1 = up (skip A), 2 = left (skip B), 3 = diag
    for x in range(1, n + 1):
        row, prow = score[x], score[x - 1]
        mrow = move[x]
        for y in range(1, m + 1):
            best, how = prow[y], 1
            if row[y - 1] > best:
                best, how = row[y - 1], 2
            s = sim(i0 + x - 1, j0 + y - 1)
            if s >= min_sim:
                cand = prow[y - 1] + (s - min_sim) + 1e-9
                if cand > best:
                    best, how = cand, 3
            row[y] = best
            mrow[y] = how
    pairs = []
    x, y = n, m
    while x > 0 and y > 0:
        how = move[x][y]
        if how == 3:
            pairs.append((i0 + x - 1, j0 + y - 1))
            x, y = x - 1, y - 1
        elif how == 1:
            x -= 1
        else:
            y -= 1
    return pairs[::-1]


def align(a: Document, b: Document, min_sim: float = 0.3, move_sim: float = 0.75) -> Alignment:
    sim = _Sim(a, b)
    na, nb = len(a.paragraphs), len(b.paragraphs)

    ca = Counter(sim.fa)
    cb = Counter(sim.fb)
    pos_b = {fp: j for j, fp in enumerate(sim.fb) if cb[fp] == 1}
    candidates = [(i, pos_b[fp]) for i, fp in enumerate(sim.fa) if ca[fp] == 1 and fp in pos_b]
    anchors = _lis(candidates)

    pairs: list[tuple[int, int]] = []
    prev_i, prev_j = 0, 0
    for i, j in anchors + [(na, nb)]:
        pairs.extend(_dp(prev_i, i, prev_j, j, sim, min_sim))
        if i < na and j < nb:
            pairs.append((i, j))
        prev_i, prev_j = i + 1, j + 1

    matched_a = {i for i, _ in pairs}
    matched_b = {j for _, j in pairs}
    left_a = [i for i in range(na) if i not in matched_a]
    left_b = [j for j in range(nb) if j not in matched_b]
    move_cands = []
    for i in left_a:
        for j in left_b:
            s = sim(i, j)
            if s >= move_sim:
                move_cands.append((-s, i, j))
    move_cands.sort()
    moves: list[tuple[int, int, float]] = []
    used_a: set[int] = set()
    used_b: set[int] = set()
    for neg, i, j in move_cands:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        moves.append((i, j, -neg))

    # Order: by B position; deletions sit right after the last kept pair before them in A.
    keyed: list[tuple[tuple[float, int, int], Op]] = []
    pair_sorted = sorted(pairs)
    a_to_b = dict(pair_sorted)
    for i, j in pair_sorted:
        s = sim(i, j)
        kind = EQUAL if s >= 1.0 else MODIFIED
        keyed.append(((j, 0, i), Op(0, kind, a.paragraphs[i].id, b.paragraphs[j].id, round(s, 3))))
    for i, j, s in moves:
        keyed.append(((j, 1, i), Op(0, MOVED, a.paragraphs[i].id, b.paragraphs[j].id, round(s, 3))))
    for j in left_b:
        if j in used_b:
            continue
        keyed.append(((j, 0, -1), Op(0, INSERTED, None, b.paragraphs[j].id, 0.0)))
    kept_a_sorted = sorted(a_to_b)
    for i in left_a:
        if i in used_a:
            continue
        k = bisect_left(kept_a_sorted, i) - 1
        jb = a_to_b[kept_a_sorted[k]] if k >= 0 else -1
        keyed.append(((jb + 0.5, 2, i), Op(0, DELETED, a.paragraphs[i].id, None, 0.0)))
    keyed.sort(key=lambda kv: kv[0])
    ops = []
    for idx, (_, op) in enumerate(keyed):
        op.index = idx
        ops.append(op)

    return Alignment(ops=ops, section_pairs=_section_pairs(a, b, ops))


def _section_pairs(a: Document, b: Document, ops: list[Op]) -> list[dict]:
    counts: dict[str, Counter] = defaultdict(Counter)
    for o in ops:
        if o.a and o.b:
            sa = a.para(o.a).section
            sb = b.para(o.b).section
            counts[sa][sb] += 1
    out = []
    for sec in a.sections:
        c = counts.get(sec.key)
        if not c:
            out.append({"a": sec.key, "b": None, "a_title": sec.title, "b_title": None, "shared": 0})
            continue
        best, n = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        bsec = next(s for s in b.sections if s.key == best)
        out.append({"a": sec.key, "b": best, "a_title": sec.title, "b_title": bsec.title, "shared": n})
    return out
