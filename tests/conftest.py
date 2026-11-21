from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docaudit import stages  # noqa: E402
from docaudit.ingest import ingest_text  # noqa: E402
from docaudit.llm.fake import FakeBackend  # noqa: E402
from docaudit.pipeline import PythonRunner, RunnerConfig  # noqa: E402

CC = "examples/planted/cc-by-4.0.txt"
PLANTED = "examples/planted/cc-by-4.0-planted.txt"
GPL2 = "examples/gpl/GPL-2.0.txt"
GPL3 = "examples/gpl/GPL-3.0.txt"
TRUTH = "examples/planted/ground_truth.json"


@pytest.fixture(autouse=True)
def _repo_cwd(monkeypatch):
    monkeypatch.chdir(ROOT)


def docs_from(a: str, b: str | None = None) -> dict:
    out = {"A": ingest_text(a, "A")}
    if b is not None:
        out["B"] = ingest_text(b, "B")
    return out


def fake_run(run_dir: Path, mode: str, a: str, b: str | None = None, concurrency: int = 4, **prep) -> dict:
    os.chdir(ROOT)
    stages.prepare(run_dir, mode, a, b, label=run_dir.name, repo_dir=ROOT, **prep)
    return PythonRunner(run_dir, FakeBackend(), config=RunnerConfig(concurrency=concurrency), log=lambda _m: None).run()


@pytest.fixture(scope="session")
def planted_diff_run(tmp_path_factory) -> Path:
    run_dir = tmp_path_factory.mktemp("runs") / "planted-diff"
    fake_run(run_dir, "diff", CC, PLANTED, skeptic_batches=4)
    return run_dir


@pytest.fixture(scope="session")
def gpl_diff_run(tmp_path_factory) -> Path:
    run_dir = tmp_path_factory.mktemp("runs") / "gpl-diff"
    fake_run(run_dir, "diff", GPL2, GPL3)
    return run_dir
