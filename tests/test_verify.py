from conftest import docs_from
from docaudit.verify import DocIndex, check_quote, verification_stats, verify_finding

A_TEXT = (
    "Section 1 -- Grant.\n\n"
    "The Licensor grants You a worldwide, non-exclusive, irrevocable license to use the Software.\n\n"
    "You must notify the Licensor within 30 days of discovering a breach of this license.\n"
)
B_TEXT = (
    "Section 1 -- Grant.\n\n"
    "The Licensor grants You a worldwide, non-exclusive, revocable license to use the Software.\n\n"
    "You must notify the Licensor within 60 days of discovering a breach of this license.\n\n"
    "You may not sublicense the Software to any third party.\n"
)


def idx():
    return DocIndex(docs_from(A_TEXT, B_TEXT))


def finding(kind, evidence, **kw):
    f = {"kind": kind, "title": "t", "description": "d", "severity": "major", "confidence": 0.8,
         "evidence": [{"doc": d, "para_id": p, "quote": q} for d, p, q in evidence]}
    f.update(kw)
    return f


def test_exact_match():
    c = check_quote(idx(), "A", "p0002", "non-exclusive, irrevocable license")
    assert c.ok and c.match == "exact" and not c.relocated


def test_exact_ignores_line_wrapping():
    c = check_quote(idx(), "A", "p0002", "irrevocable\n   license to use")
    assert c.ok and c.match == "exact"


def test_normalized_match_quotes_case_hyphen_dash():
    ix = DocIndex(docs_from('The \u201cLicensed Material\u201d is non-exclusive \u2013 see below.\n'))
    c = check_quote(ix, "A", "p0001", 'the "licensed material" is nonexclusive - see below')
    assert c.ok and c.match == "normalized"


def test_elided_match_in_order_only():
    ix = idx()
    ok = check_quote(ix, "A", "p0003", "You must notify ... discovering a breach")
    assert ok.ok and ok.match == "elided"
    wrong_order = check_quote(ix, "A", "p0003", "discovering a breach ... You must notify")
    assert not wrong_order.ok


def test_fabricated_quote_rejected_with_diagnostic():
    c = check_quote(idx(), "A", "p0003", "You must notify the Licensor by registered mail within 30 days")
    assert not c.ok and c.reason.startswith("quote_not_found") and 0 < c.common < 1


def test_too_short_quote_rejected():
    c = check_quote(idx(), "A", "p0002", "the")
    assert not c.ok and c.reason == "quote_too_short"


def test_wrong_paragraph_id_is_reattributed():
    c = check_quote(idx(), "A", "p0002", "within 30 days of discovering")
    assert c.ok and c.relocated and c.found_para == "p0003"


def test_quote_only_in_other_document_rejected():
    c = check_quote(idx(), "A", "p0002", "You may not sublicense the Software")
    assert not c.ok and c.reason.startswith("quote_in_other_doc_only")


def test_unknown_paragraph_and_document():
    ix = idx()
    assert check_quote(ix, "A", "p0999", "within 30 days of discovering").relocated
    assert not check_quote(ix, "C", "p0001", "anything at all here").ok


def test_finding_rejected_when_any_quote_fails():
    v = verify_finding(finding("changed", [("A", "p0003", "within 30 days of discovering"),
                                           ("B", "p0003", "within 90 days of discovering")]), "reader-c01", "diff", idx())
    assert v.status == "rejected" and v.code == "quote_not_found"
    assert len(v.evidence) == 2 and v.evidence[0].ok and not v.evidence[1].ok


def test_changed_accepted():
    v = verify_finding(finding("changed", [("A", "p0003", "within 30 days"), ("B", "p0003", "within 60 days")]), "r", "diff", idx())
    assert v.status == "accepted"


def test_changed_without_difference_rejected():
    v = verify_finding(finding("changed", [("A", "p0003", "You must notify the Licensor"),
                                           ("B", "p0003", "You must notify the Licensor")]), "r", "diff", idx())
    assert v.status == "rejected" and v.code == "changed_without_difference"


def test_added_text_already_in_a_rejected():
    v = verify_finding(finding("added", [("B", "p0002", "The Licensor grants You a worldwide")]), "r", "diff", idx())
    assert v.status == "rejected" and v.code == "added_text_present_in_A"
    ok = verify_finding(finding("added", [("B", "p0004", "You may not sublicense the Software")]), "r", "diff", idx())
    assert ok.status == "accepted"


def test_removed_text_still_in_b_rejected():
    v = verify_finding(finding("removed", [("A", "p0003", "You must notify the Licensor")]), "r", "diff", idx())
    assert v.status == "rejected" and v.code == "removed_text_present_in_B"


def test_schema_kind_and_mode_checks():
    ix = idx()
    bad = finding("changed", [("A", "p0003", "within 30 days")])
    del bad["severity"]
    assert verify_finding(bad, "r", "diff", ix).code == "schema_invalid"
    assert verify_finding(finding("added", [("A", "p0003", "within 30 days")]), "r", "audit",
                          DocIndex(docs_from(A_TEXT))).code == "kind_not_allowed_in_audit_mode"
    assert verify_finding(finding("ambiguity", [("A", "p0003", "within 30 days")]), "r", "audit",
                          DocIndex(docs_from(A_TEXT))).status == "accepted"
    assert verify_finding(finding("changed", []), "r", "diff", ix).code == "no_evidence"


def test_confidence_is_clamped_with_a_note():
    v = verify_finding(finding("changed", [("A", "p0003", "within 30 days"), ("B", "p0003", "within 60 days")], confidence=1.7),
                       "r", "diff", idx())
    assert v.status == "accepted" and v.confidence == 1.0 and any("clamped" in n for n in v.notes)


def test_stats_separate_sweeps_from_agents():
    ix = idx()
    vs = [
        verify_finding(finding("changed", [("A", "p0003", "within 30 days"), ("B", "p0003", "within 60 days")]), "reader-c01", "diff", ix),
        verify_finding(finding("changed", [("A", "p0003", "made up text that is not there")]), "reader-c01", "diff", ix),
        verify_finding(finding("broken_reference", [("B", "p0001", "Section 1 -- Grant.")]), "sweep", "diff", ix),
    ]
    st = verification_stats(vs)
    assert st["agent_findings"] == 2 and st["rejected"] == 1 and st["rejection_rate"] == 0.5 and st["sweep_findings"] == 1
