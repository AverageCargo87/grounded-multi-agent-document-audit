"""Run the Claude Code Workflow script offline: real script, mocked hooks, FakeLLM agents.

The mock agent() executes the build-step commands the script asks for and
simulates each role agent with `python -m docaudit fake-agent`, so the
script's control flow, prompts, file contract and concurrency cap are all
exercised. The resulting report must equal the Python runner's report on an
identically prepared run directory.
"""

import json
import shutil
import subprocess
import sys

import pytest

from conftest import CC, PLANTED, ROOT, fake_run
from docaudit import stages
from docaudit.runstore import Run

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="node is not installed")


def run_mock(run_dir, tmp_path):
    args_path = run_dir / "workflow_args.json"
    stats_path = tmp_path / "stats.json"
    out = subprocess.run([NODE, str(ROOT / "tests/js/run_workflow_mock.mjs"), str(ROOT / "workflow/document-audit.workflow.js"),
                          str(args_path), str(stats_path)], cwd=ROOT, capture_output=True, text=True, timeout=300)
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    assert out.returncode == 0, stats["errors"]
    return stats


def comparable(report):
    report = dict(report)
    report.pop("run")
    pipe = dict(report.pop("pipeline"))
    for k in ("usage", "agent_failures", "incomplete"):
        pipe.pop(k)
    report["pipeline"] = pipe
    return report


def test_workflow_matches_python_runner_and_respects_concurrency_cap(tmp_path):
    wf_dir = tmp_path / "wf"
    stages.prepare(wf_dir, "diff", CC, PLANTED, label="eq", skeptic_batches=4, python=sys.executable, repo_dir=ROOT)
    stats = run_mock(wf_dir, tmp_path)
    assert stats["maxActive"] <= 2
    assert stats["maxActive"] == 2  # the cap is reached, not just respected
    assert stats["phases"] == ["Read", "Verify", "Gaps", "Skeptics", "Recheck", "Edit", "Report"]
    assert {"reader-c01", "crossref", "verify", "gap", "skeptic-b01-v1", "aggregate", "editor", "report"} <= set(stats["calls"])

    py_dir = tmp_path / "py"
    fake_run(py_dir, "diff", CC, PLANTED, skeptic_batches=4)
    a, b = Run(wf_dir), Run(py_dir)
    assert a.read_json("report.json")["run"]["runner"] == "workflow"
    assert comparable(a.read_json("report.json")) == comparable(b.read_json("report.json"))
    for p in sorted((wf_dir / "agents").glob("*.json")):
        assert p.read_text(encoding="utf-8") == (py_dir / "agents" / p.name).read_text(encoding="utf-8"), p.name


def test_workflow_audit_mode_matches_python_runner_and_skips_empty_batches(tmp_path):
    # 3 findings over 4 fixed batches leaves batch b04 empty: neither runner may start a skeptic for it.
    wf_dir = tmp_path / "wf-audit"
    stages.prepare(wf_dir, "audit", PLANTED, label="eq-audit", skeptic_batches=4, python=sys.executable, repo_dir=ROOT)
    stats = run_mock(wf_dir, tmp_path)
    assert stats["maxActive"] <= 2
    assert "Gaps" not in stats["phases"]
    assert Run(wf_dir).read_json("skeptic/b04.json")["finding_ids"] == []
    assert "skeptic-b04-v1" not in stats["calls"]

    py_dir = tmp_path / "py-audit"
    fake_run(py_dir, "audit", PLANTED, skeptic_batches=4)
    wf_agents = sorted(p.name for p in (wf_dir / "agents").glob("*.json"))
    assert wf_agents == sorted(p.name for p in (py_dir / "agents").glob("*.json"))
    for name in wf_agents:
        assert (wf_dir / "agents" / name).read_text(encoding="utf-8") == (py_dir / "agents" / name).read_text(encoding="utf-8"), name
    assert comparable(Run(wf_dir).read_json("report.json")) == comparable(Run(py_dir).read_json("report.json"))


def test_workflow_rejects_missing_args(tmp_path):
    bad = tmp_path / "args.json"
    bad.write_text(json.dumps({"runDir": str(tmp_path)}), encoding="utf-8")
    stats_path = tmp_path / "stats.json"
    out = subprocess.run([NODE, str(ROOT / "tests/js/run_workflow_mock.mjs"), str(ROOT / "workflow/document-audit.workflow.js"),
                          str(bad), str(stats_path)], cwd=ROOT, capture_output=True, text=True, timeout=60)
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    assert out.returncode == 1 and "args.repoDir is required" in stats["errors"][0]
    assert stats["calls"] == []
