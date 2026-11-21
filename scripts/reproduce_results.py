"""Regenerate every committed result under examples/results/ from scratch.

All of it is offline and deterministic: the no-LLM baseline and FakeLLM
fixture runs. Real model runs are not produced here.

    python scripts/reproduce_results.py          # rewrite examples/results/
    python scripts/reproduce_results.py --check  # fail if the committed files differ

Run directories go to runs/ (git-ignored); only reports and scores are copied.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docaudit import stages  # noqa: E402
from docaudit.evaluation import baseline, score  # noqa: E402
from docaudit.llm.fake import FakeBackend  # noqa: E402
from docaudit.pipeline import PythonRunner  # noqa: E402

TRUTH = "examples/planted/ground_truth.json"
RUNS = [
    {"label": "planted-diff-fixture", "mode": "diff", "a": "examples/planted/cc-by-4.0.txt",
     "b": "examples/planted/cc-by-4.0-planted.txt", "score": True},
    {"label": "planted-audit-fixture", "mode": "audit", "a": "examples/planted/cc-by-4.0-planted.txt", "b": None, "score": True},
    {"label": "gpl-v2-v3-fixture", "mode": "diff", "a": "examples/gpl/GPL-2.0.txt", "b": "examples/gpl/GPL-3.0.txt", "score": False},
]


def build(out_root: Path) -> None:
    for spec in RUNS:
        run_dir = ROOT / "runs" / spec["label"]
        if run_dir.exists():
            shutil.rmtree(run_dir)
        stages.prepare(run_dir, spec["mode"], spec["a"], spec["b"], label=spec["label"], skeptic_batches=4, repo_dir=ROOT)
        PythonRunner(run_dir, FakeBackend(), log=lambda _m: None).run()
        dest = out_root / spec["label"]
        dest.mkdir(parents=True, exist_ok=True)
        for name in ("report.md", "report.json"):
            shutil.copyfile(run_dir / name, dest / name)
        if spec["score"]:
            baseline(run_dir)
            for source in ("baseline", "final"):
                result = score(run_dir, TRUTH, source=source)
                name = "score-baseline.json" if source == "baseline" else "score-fixture.json"
                (dest / name).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    import os
    os.chdir(ROOT)
    committed = ROOT / "examples" / "results"
    if not args.check:
        build(committed)
        print(f"wrote {committed.relative_to(ROOT)}")
        return 0
    tmp = ROOT / "runs" / "_check_results"
    if tmp.exists():
        shutil.rmtree(tmp)
    build(tmp)
    diffs = []
    for f in sorted(tmp.rglob("*")):
        if f.is_file():
            rel = f.relative_to(tmp)
            c = committed / rel
            if not c.exists() or c.read_bytes() != f.read_bytes():
                diffs.append(str(rel))
    print("OK" if not diffs else "DIFFERENT: " + ", ".join(diffs))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
