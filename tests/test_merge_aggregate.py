from conftest import docs_from
from docaudit.aggregate import aggregate, apply_verdicts
from docaudit.align import align
from docaudit.merge import coverage, merge_findings, noisy_or
from docaudit.verify import DocIndex, verify_finding

A_TEXT = (
    "Clause one: the supplier delivers within ten days of the order.\n\n"
    "Clause two: the buyer pays within thirty days of delivery, and late payment carries interest.\n\n"
    "Clause three: notices go by registered mail.\n"
)
B_TEXT = (
    "Clause one: the supplier delivers within ten days of the order.\n\n"
    "Clause two: the buyer pays within sixty days of delivery, and late payment carries no interest.\n\n"
    "Clause three: notices go by registered mail.\n"
)


def setup():
    docs = docs_from(A_TEXT, B_TEXT)
    return docs, DocIndex(docs), align(docs["A"], docs["B"])


def f(kind, ev, title="t", desc="d", sev="major", conf=0.7):
    return {"kind": kind, "title": title, "description": desc, "severity": sev, "confidence": conf,
            "evidence": [{"doc": d, "para_id": p, "quote": q} for d, p, q in ev]}


def accepted(raws, ix):
    out = [verify_finding(r, src, "diff", ix) for src, r in raws]
    assert all(v.status == "accepted" for v in out), [v.reasons for v in out]
    return out


# ---------------------------------------------------------------- merge


def test_same_change_from_two_agents_is_merged():
    docs, ix, al = setup()
    vs = accepted([
        ("reader-c01", f("changed", [("A", "p0002", "pays within thirty days"), ("B", "p0002", "pays within sixty days")],
                         title="Payment term doubled", sev="major", conf=0.7)),
        ("crossref", f("changed", [("A", "p0002", "within thirty days of delivery"), ("B", "p0002", "within sixty days of delivery")],
                       title="Value changed: thirty to sixty", sev="minor", conf=0.6)),
    ], ix)
    merged = merge_findings(vs, docs, al)
    assert len(merged) == 1
    m = merged[0]
    assert m.id == "F001" and m.members == 2 and m.sources == ["crossref", "reader-c01"]
    assert m.severity == "major" and m.title == "Payment term doubled"
    assert m.confidence == noisy_or([0.7, 0.6]) == 0.88
    assert len(m.evidence) == 4


def test_change_and_defect_on_same_paragraph_stay_separate():
    docs, ix, al = setup()
    vs = accepted([
        ("reader-c01", f("changed", [("A", "p0002", "pays within thirty days"), ("B", "p0002", "pays within sixty days")])),
        ("crossref", f("inconsistent_value", [("B", "p0002", "pays within sixty days")], title="Payment term conflicts")),
    ], ix)
    assert len(merge_findings(vs, docs, al)) == 2


def test_different_issues_in_same_paragraph_stay_separate():
    docs, ix, al = setup()
    vs = accepted([
        ("reader-c01", f("changed", [("A", "p0002", "pays within thirty days"), ("B", "p0002", "pays within sixty days")],
                         title="Payment term doubled", desc="The buyer has twice as long to pay.")),
        ("reader-c02", f("changed", [("A", "p0002", "late payment carries interest"), ("B", "p0002", "late payment carries no interest")],
                         title="Late interest removed", desc="Interest on overdue invoices no longer applies.")),
    ], ix)
    merged = merge_findings(vs, docs, al)
    assert [m.title for m in merged] == ["Late interest removed", "Payment term doubled"]
    assert [m.id for m in merged] == ["F001", "F002"]


def test_coverage_counts_cited_changed_ops():
    docs, ix, al = setup()
    assert coverage(al, [])["uncovered"] == [o.index for o in al.changed_ops()]
    cov = coverage(al, [{"evidence": [{"doc": "B", "para_id": "p0002"}]}])
    assert cov == {"changed_ops": 1, "covered": 1, "ratio": 1.0, "uncovered": []}


# ---------------------------------------------------------------- skeptic aggregation

BASE = {"id": "F001", "kind": "changed", "title": "t", "description": "d", "severity": "major", "confidence": 0.8,
        "evidence": [{"doc": "A", "para_id": "p0002", "quote": "pays within thirty days"}], "sources": ["reader-c01"], "position": [1]}


def verdict(v, sev="keep", ce=(), fid="F001"):
    return {"finding_id": fid, "verdict": v, "reason": "r", "suggested_severity": sev,
            "counter_evidence": [{"doc": d, "para_id": p, "quote": q} for d, p, q in ce]}


GOOD_CE = [("B", "p0002", "pays within sixty days")]
BAD_CE = [("B", "p0002", "this sentence does not exist anywhere")]


def run_agg(verdicts, finding=BASE, low=0.25):
    _, ix, _ = setup()
    return aggregate([dict(finding)], [(f"skeptic-{i}", v) for i, v in enumerate(verdicts)], ix, low_confidence=low)


def test_upheld_boosts_confidence():
    out = run_agg([verdict("upheld")])
    (g,) = out["findings"]
    assert g["status"] == "upheld" and g["confidence"] == 0.85 and g["severity"] == "major"


def test_grounded_majority_refutation_kills():
    out = run_agg([verdict("refuted", ce=GOOD_CE), verdict("refuted", ce=GOOD_CE), verdict("upheld")])
    assert out["findings"] == [] and out["killed"][0]["status"] == "killed"


def test_ungrounded_refutation_cannot_kill():
    out = run_agg([verdict("refuted", ce=BAD_CE)])
    (g,) = out["findings"]
    assert g["status"] == "downgraded" and g["severity"] == "minor"
    assert g["verdicts"][0]["effective"] == "weakened"
    assert out["verdict_stats"]["ungrounded_refutations"] == 1


def test_minority_refutation_downgrades():
    out = run_agg([verdict("refuted", ce=GOOD_CE), verdict("upheld"), verdict("upheld")])
    (g,) = out["findings"]
    assert g["status"] == "downgraded" and g["severity"] == "minor" and g["confidence"] == 0.48


def test_weakened_uses_suggested_severity_or_keep():
    (g,) = run_agg([verdict("weakened", sev="info", ce=GOOD_CE)])["findings"]
    assert g["severity"] == "info"
    (g,) = run_agg([verdict("weakened", sev="keep", ce=GOOD_CE)])["findings"]
    assert g["severity"] == "major" and g["status"] == "downgraded"
    # Naming the current severity is the same as keep, not a hidden one-level cut.
    (g,) = run_agg([verdict("weakened", sev="major", ce=GOOD_CE)])["findings"]
    assert g["severity"] == "major" and g["status"] == "downgraded"


def test_skeptic_cannot_raise_severity():
    (g,) = run_agg([verdict("weakened", sev="critical", ce=GOOD_CE)])["findings"]
    assert g["severity"] == "minor"


def test_no_verdict_means_unreviewed():
    (g,) = run_agg([])["findings"]
    assert g["status"] == "unreviewed" and g["confidence"] == 0.64


def test_low_confidence_bucket_and_unknown_ids():
    finding = dict(BASE, confidence=0.3)
    out = run_agg([verdict("weakened", ce=GOOD_CE), verdict("upheld", fid="F999")], finding=finding)
    assert out["findings"] == [] and out["low_confidence"][0]["confidence"] == 0.18
    assert out["verdict_stats"]["unknown_finding_ids"] == ["F999"]


def test_invalid_verdict_is_ignored():
    _, ix, _ = setup()
    out = aggregate([dict(BASE)], [("skeptic-x", {"finding_id": "F001", "verdict": "maybe"})], ix)
    assert out["findings"][0]["status"] == "unreviewed"


def test_apply_verdicts_keeps_original_values():
    g = apply_verdicts(dict(BASE), [{"effective": "upheld", "suggested_severity": "keep"}])
    assert g["original_severity"] == "major" and g["original_confidence"] == 0.8
