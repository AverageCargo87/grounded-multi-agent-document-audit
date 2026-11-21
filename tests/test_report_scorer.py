import json
import re
import subprocess
import sys

from conftest import ROOT, TRUTH
from docaudit.evaluation import baseline, resolve_anchor, score
from docaudit.ingest import ingest_file
from docaudit.report import build_report
from docaudit.runstore import Run

# ---------------------------------------------------------------- report


def test_every_link_in_the_markdown_has_an_anchor(planted_diff_run):
    md = Run(planted_diff_run).read_text("report.md")
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', md))
    links = set(re.findall(r"\]\(#([a-z]-p\d{4})\)", md))
    assert links and links <= anchors


def test_report_sections_and_order(planted_diff_run):
    rep = Run(planted_diff_run).read_json("report.json")
    md = Run(planted_diff_run).read_text("report.md")
    for heading in ("## Pipeline", "## Summary", "## Findings", "## Refuted by skeptics", "## Cited paragraphs"):
        assert heading in md
    sev = {"critical": 0, "major": 1, "minor": 2, "info": 3}
    killed = {f["id"] for f in rep["killed"]}
    assert not killed & {f["id"] for f in rep["findings"]}
    ranks = [sev[f["severity"]] for f in rep["findings"]]
    assert ranks == sorted(ranks)  # the fake editor keeps code order


def test_editor_cannot_resurrect_or_invent(planted_diff_run, tmp_path):
    import shutil
    run_dir = tmp_path / "copy"
    shutil.copytree(planted_diff_run, run_dir)
    run = Run(run_dir)
    agg = run.read_json("aggregated.json")
    killed_id = agg["killed"][0]["id"]
    first = agg["findings"][0]["id"]
    run.write_json("agents/editor.json", {
        "executive_summary": f"See {first} and F999. The text says \"the Licensor promises to pay damages to everyone\".",
        "themes": [{"title": "Mixed", "finding_ids": [first, killed_id, "F999"]}],
        "ordered_finding_ids": [killed_id, "F999", first],
    })
    rep = build_report(run_dir)
    issues = " | ".join(rep["summary"]["issues"])
    assert f"refuted finding {killed_id}" in issues and "unknown id F999" in issues
    assert "not a surviving finding" in issues and "were not found in the documents" in issues
    assert rep["summary"]["unverified_quotes"] == ["the Licensor promises to pay damages to everyone"]
    assert rep["findings"][0]["id"] == first
    assert rep["summary"]["themes"] == [{"title": "Mixed", "finding_ids": [first]}]
    assert {f["id"] for f in rep["findings"]} == {f["id"] for f in agg["findings"]}


def test_missing_editor_falls_back_to_code_order(planted_diff_run, tmp_path):
    import shutil
    run_dir = tmp_path / "noeditor"
    shutil.copytree(planted_diff_run, run_dir)
    (run_dir / "agents" / "editor.json").unlink()
    rep = build_report(run_dir)
    assert rep["summary"]["issues"] == ["editor output missing: findings are listed in default order"]
    assert [f["id"] for f in rep["findings"]] == [f["id"] for f in Run(run_dir).read_json("aggregated.json")["findings"]]


# ---------------------------------------------------------------- scorer


def test_ground_truth_anchors_resolve_uniquely():
    truth = json.loads((ROOT / TRUTH).read_text(encoding="utf-8"))
    a, b = ingest_file(truth["base"], "A"), ingest_file(truth["fixture"], "B")
    for it in truth["items"]:
        for x in it.get("anchors_a", []):
            resolve_anchor(a, x)
        for x in it.get("anchors_b", []) + it.get("audit_anchors", []):
            resolve_anchor(b, x)
    assert sum(it["substantive"] for it in truth["items"]) == 13
    assert sum("audit" in it["modes"] for it in truth["items"]) == 4


def test_baseline_score_on_planted_diff(planted_diff_run):
    baseline(planted_diff_run)
    s = score(planted_diff_run, TRUTH, source="baseline")
    assert s["recall"] == 1.0 and s["findings_correct"] == 13 and s["findings_wrong"] == 2
    assert s["editorial_items_flagged"] == ["E01", "E04"] and s["findings_on_ignored_items"] == 1
    assert s["precision"] == round(13 / 15, 4)


def test_scorer_counts_kills_info_and_ignored(planted_diff_run, tmp_path):
    import shutil
    run_dir = tmp_path / "synthetic"
    shutil.copytree(planted_diff_run, run_dir)
    run = Run(run_dir)
    rep = run.read_json("report.json")
    b = run.docs["B"]
    p01 = resolve_anchor(b, "cured within 60 days")
    p05 = resolve_anchor(b, "non-exclusive, revocable license")
    banner = resolve_anchor(b, "EVALUATION FIXTURE")
    e01 = resolve_anchor(b, "Patent and trademark rights are not licenced")

    def f(fid, pid, sev="major"):
        return {"id": fid, "kind": "changed", "title": fid, "severity": sev, "evidence": [{"doc": "B", "para_id": pid, "quote": "x"}]}

    rep["findings"] = [f("F1", p01), f("F2", banner), f("F3", e01, sev="info"), f("F4", e01)]
    rep["low_confidence"] = []
    rep["killed"] = [f("F5", p05)]
    run.write_json("report.json", rep)
    s = score(run_dir, TRUTH)
    assert s["found"] == ["P01"] and s["skeptic_false_kills"] == ["P05"]
    assert s["findings_on_ignored_items"] == 1 and s["findings_info_excluded"] == 1
    assert s["findings_correct"] == 1 and s["findings_wrong"] == 1 and s["editorial_items_flagged"] == ["E01"]


def test_audit_scoring_requires_matching_kind(tmp_path):
    from conftest import PLANTED, fake_run
    run_dir = tmp_path / "audit"
    fake_run(run_dir, "audit", PLANTED)
    run = Run(run_dir)
    rep = run.read_json("report.json")
    a = run.docs["A"]
    pid = resolve_anchor(a, "terminated under Section 9(a), it reinstates")
    rep["findings"] = [{"id": "F1", "kind": "ambiguity", "title": "x", "severity": "major",
                        "evidence": [{"doc": "A", "para_id": pid, "quote": "x"}]}]
    rep["low_confidence"], rep["killed"] = [], []
    run.write_json("report.json", rep)
    s = score(run_dir, TRUTH)
    assert "P07" not in s["found"] and s["findings_wrong"] == 1


def test_committed_results_are_reproducible():
    out = subprocess.run([sys.executable, "scripts/reproduce_results.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr


def test_planted_fixture_is_up_to_date():
    out = subprocess.run([sys.executable, "scripts/make_planted.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0 and out.stdout.strip() == "OK"
