"""Severity and confidence aggregation: the skeptics get the last word.

Rules, applied per finding over all skeptic verdicts that name it:

1. Counter-evidence is quote-verified like any other evidence. A "refuted"
   verdict without at least one verified counter-quote is treated as
   "weakened" (an ungrounded refutation cannot kill a grounded finding).
2. No verdicts (skeptic stage skipped or failed): status ``unreviewed``,
   confidence x 0.8.
3. Grounded refutations from a strict majority of skeptics: status ``killed``.
   The finding leaves the report body and is listed with the refutation.
4. Otherwise, any refutation or weakening: status ``downgraded`` and
   confidence x 0.6. Severity drops to the lowest severity any non-upholding
   skeptic suggests; a refutation (minority or ungrounded) that suggests
   nothing lower costs one level; a "weakened" verdict with "keep" (or the
   current severity) leaves severity unchanged.
5. All skeptics uphold: status ``upheld``, confidence c -> c + (1 - c) x 0.25.

Skeptics can never raise severity, and the editor that runs afterwards cannot
change severity or confidence at all.
"""

from __future__ import annotations

from .schemas import SEVERITIES, VERDICT, validate
from .verify import DocIndex, check_quote

SEV_INDEX = {s: i for i, s in enumerate(SEVERITIES)}  # critical=0 ... info=3

UNREVIEWED_FACTOR = 0.8
DOWNGRADE_FACTOR = 0.6
UPHOLD_BOOST = 0.25


def lower(severity: str, steps: int = 1) -> str:
    return SEVERITIES[min(len(SEVERITIES) - 1, SEV_INDEX[severity] + steps)]


def effective_verdicts(raw_verdicts: list[tuple[str, dict]], index: DocIndex) -> list[dict]:
    """Validate verdicts and verify their counter-evidence."""
    out = []
    for source, v in raw_verdicts:
        errors = validate(v, VERDICT)
        if errors:
            out.append({"source": source, "finding_id": v.get("finding_id") if isinstance(v, dict) else None,
                        "verdict": "invalid", "effective": "invalid", "reason": "; ".join(errors[:2]),
                        "suggested_severity": "keep", "counter_evidence": [], "notes": ["schema_invalid"]})
            continue
        checks = [check_quote(index, e["doc"], e["para_id"], e["quote"]) for e in v["counter_evidence"]]
        ok = [c for c in checks if c.ok]
        effective = v["verdict"]
        notes = []
        if v["verdict"] == "refuted" and not ok:
            effective = "weakened"
            notes.append("ungrounded refutation: no verified counter-evidence, treated as weakened")
        bad = [c for c in checks if not c.ok]
        if bad:
            notes.append(f"{len(bad)} counter-quote(s) failed verification")
        out.append({
            "source": source,
            "finding_id": v["finding_id"],
            "verdict": v["verdict"],
            "effective": effective,
            "reason": v["reason"].strip(),
            "suggested_severity": v["suggested_severity"],
            "counter_evidence": [{"doc": c.doc, "para_id": c.found_para or c.para_id, "quote": c.quote, "verified": c.ok} for c in checks],
            "notes": notes,
        })
    return out


def apply_verdicts(finding: dict, verdicts: list[dict]) -> dict:
    f = dict(finding)
    vs = [v for v in verdicts if v["effective"] in ("upheld", "weakened", "refuted")]
    f["verdicts"] = verdicts
    sev, conf = f["severity"], f["confidence"]
    f["original_severity"] = sev
    f["original_confidence"] = conf
    if not vs:
        f["status"] = "unreviewed"
        f["confidence"] = round(conf * UNREVIEWED_FACTOR, 4)
        return f
    refuted = sum(v["effective"] == "refuted" for v in vs)
    weakened = sum(v["effective"] == "weakened" for v in vs)
    if refuted * 2 > len(vs):
        f["status"] = "killed"
        return f
    if refuted or weakened:
        candidates = []
        for v in vs:
            if v["effective"] == "upheld":
                continue
            s = v["suggested_severity"]
            if s in SEV_INDEX and SEV_INDEX[s] > SEV_INDEX[sev]:
                candidates.append(s)  # a lower severity the skeptic would accept
            elif s in ("keep", sev) and v["verdict"] == "weakened":
                candidates.append(sev)  # real but overstated in scope only (naming the current severity means keep)
            else:
                candidates.append(lower(sev))  # refutations (minority or ungrounded) always cost one level
        f["severity"] = max(candidates, key=lambda s: SEV_INDEX[s])
        f["confidence"] = round(conf * DOWNGRADE_FACTOR, 4)
        f["status"] = "downgraded"
        return f
    f["status"] = "upheld"
    f["confidence"] = round(min(0.99, conf + (1.0 - conf) * UPHOLD_BOOST), 4)
    return f


def aggregate(findings: list[dict], raw_verdicts: list[tuple[str, dict]], index: DocIndex,
              low_confidence: float = 0.25) -> dict:
    eff = effective_verdicts(raw_verdicts, index)
    known = {f["id"] for f in findings}
    by_id: dict[str, list[dict]] = {}
    unknown = []
    for v in eff:
        if v["finding_id"] in known:
            by_id.setdefault(v["finding_id"], []).append(v)
        else:
            unknown.append(v)
    main, low, killed = [], [], []
    for f in findings:
        g = apply_verdicts(f, by_id.get(f["id"], []))
        if g["status"] == "killed":
            killed.append(g)
        elif g["confidence"] < low_confidence:
            low.append(g)
        else:
            main.append(g)

    def rank(f: dict) -> tuple:
        return (SEV_INDEX[f["severity"]], -f["confidence"], f["position"], f["id"])

    main.sort(key=rank)
    low.sort(key=rank)
    killed.sort(key=lambda f: f["id"])
    statuses: dict[str, int] = {}
    for f in main + low + killed:
        statuses[f["status"]] = statuses.get(f["status"], 0) + 1
    return {
        "findings": main,
        "low_confidence": low,
        "killed": killed,
        "verdict_stats": {
            "verdicts": len(eff),
            "by_verdict": _count(v["verdict"] for v in eff),
            "by_effective": _count(v["effective"] for v in eff),
            "ungrounded_refutations": sum(1 for v in eff if v["verdict"] == "refuted" and v["effective"] == "weakened"),
            "unknown_finding_ids": [v["finding_id"] for v in unknown],
        },
        "status_counts": dict(sorted(statuses.items())),
    }


def _count(values) -> dict[str, int]:
    out: dict[str, int] = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))
