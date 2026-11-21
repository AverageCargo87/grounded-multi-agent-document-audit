import pytest

from conftest import CC, PLANTED
from docaudit.ingest import ingest_file, ingest_text
from docaudit.prompts import all_role_systems
from docaudit.schemas import FINDING, RECEIPT, ROLE_SCHEMAS, SHELL_RESULT, validate, validate_role_output
from docaudit.sweeps import defined_terms, find_references, numbering_gaps, sweep_findings
from docaudit.workflow_assets import check_or_write

ALL = list(ROLE_SCHEMAS.values()) + [RECEIPT, SHELL_RESULT]


def walk(schema):
    yield schema
    for sub in schema.get("properties", {}).values():
        yield from walk(sub)
    if "items" in schema:
        yield from walk(schema["items"])


def test_schemas_fit_the_structured_output_subset():
    banned = {"minimum", "maximum", "minLength", "maxLength", "multipleOf", "pattern", "minItems", "maxItems"}
    for schema in ALL:
        for node in walk(schema):
            assert not banned & set(node), node
            if node.get("type") == "object":
                assert node.get("additionalProperties") is False
                assert set(node["required"]) == set(node["properties"])


def test_schemas_are_valid_json_schema():
    jsonschema = pytest.importorskip("jsonschema")
    for schema in ALL:
        jsonschema.Draft202012Validator.check_schema(schema)


def test_validator_agrees_with_jsonschema():
    jsonschema = pytest.importorskip("jsonschema")
    good = {"kind": "changed", "title": "t", "description": "d", "severity": "minor", "confidence": 0.5,
            "evidence": [{"doc": "A", "para_id": "p0001", "quote": "q"}]}
    bad = [dict(good, kind="nope"), dict(good, confidence="high"), {k: v for k, v in good.items() if k != "title"},
           dict(good, extra=1), dict(good, evidence=[{"doc": "A", "para_id": "p0001"}]), dict(good, confidence=True)]
    v = jsonschema.Draft202012Validator(FINDING)
    assert validate(good, FINDING) == [] and v.is_valid(good)
    for b in bad:
        assert validate(b, FINDING) and not v.is_valid(b), b


def test_role_outputs_validate():
    assert validate_role_output("skeptic", {"verdicts": [], "missed": []}) == []
    assert validate_role_output("editor", {"executive_summary": "s", "themes": [], "ordered_finding_ids": []}) == []
    assert validate_role_output("section_reader", {"findings": []})


def test_prompts_cover_every_role_and_mode():
    systems = all_role_systems()
    assert set(systems) == set(ROLE_SCHEMAS)
    for role, modes in systems.items():
        assert set(modes) == {"audit", "diff"}
        if role != "editor":
            assert "Evidence rules" in modes["diff"] and "added" in modes["diff"] and "contradiction" in modes["audit"]


def test_workflow_script_embeds_current_schemas_and_prompts():
    assert check_or_write(write=False), "run: python -m docaudit export-workflow-assets"


# ---------------------------------------------------------------- deterministic sweeps


def test_cross_references_resolve_on_clean_text():
    refs = find_references(ingest_file(CC))
    assert len(refs) >= 15 and all(r.status == "ok" for r in refs)
    assert any(r.text == "Section 3(a)(1)(A)(i)" for r in refs)


def test_dangling_reference_and_numbering_gap_found_in_planted_copy():
    a, b = ingest_file(CC, "A"), ingest_file(PLANTED, "B")
    found = sweep_findings(b, baseline_doc=a)
    kinds = sorted((f["kind"], f["title"]) for f in found)
    assert kinds == [("broken_reference", "Cross-reference to a non-existent target: Section 9(a)"),
                     ("omission", "Numbering gap: item 3 is missing")]
    assert sweep_findings(a) == []


def test_numbering_gap_handles_roman_and_letters():
    text = ("Section 1 -- Things.\n\n  a. first\n\n       i. one\n\n      ii. two\n\n      iv. four\n\n  b. second\n\n  d. fourth\n")
    gaps = numbering_gaps(ingest_text(text))
    assert sorted((g["expected"], g["found"]) for g in gaps) == [("c", "d"), ("iii", "iv")]


def test_multi_section_reference_list():
    text = "Section 1 -- A.\n\nx\n\nSection 2 -- B.\n\nSections 1, 2, and 7 survive termination.\n"
    refs = find_references(ingest_text(text))
    assert sorted((r.section, r.status) for r in refs) == [("1", "ok"), ("2", "ok"), ("7", "dangling")]


def test_defined_terms_detected():
    terms = defined_terms(ingest_file(CC))
    for t in ("Adapted Material", "Licensed Rights", "Licensor", "Public License"):
        assert t in terms
