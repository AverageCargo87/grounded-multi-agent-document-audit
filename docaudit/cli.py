"""Command line interface: ``python -m docaudit <command>``.

Deterministic stages (used by both runners and by the workflow's shell steps):
  prepare, verify, recheck-prep, aggregate, report, validate
Runners:
  run            the Python runner (backend: fake or anthropic)
  fake-agent     one FakeLLM agent call (used by the offline workflow test)
Evaluation:
  baseline, score
Maintenance:
  export-workflow-assets
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, stages
from .stages import summary_line


def _add_prepare_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--mode", choices=["audit", "diff"], required=True)
    p.add_argument("--a", required=True, help="document to audit, or version A in diff mode")
    p.add_argument("--b", help="version B (diff mode)")
    p.add_argument("--run", required=True, help="run directory to create")
    p.add_argument("--label", help="label shown in the report (default: run directory name)")
    p.add_argument("--chunk-chars", type=int, help="target characters per section-reader chunk (default 12000)")
    p.add_argument("--skeptic-batch-size", type=int, help="findings per skeptic batch (default 12)")
    p.add_argument("--skeptic-batches", type=int, help="fixed number of skeptic batches (the workflow uses 4)")
    p.add_argument("--skeptic-votes", type=int, help="independent skeptics per batch (default 1)")
    p.add_argument("--python", default="python", help="python command the workflow's shell steps should use")


def _prepare(args) -> dict:
    return stages.prepare(args.run, args.mode, args.a, args.b, label=args.label, python=args.python,
                          chunk_chars=args.chunk_chars, skeptic_batch_size=args.skeptic_batch_size,
                          skeptic_batches=args.skeptic_batches, skeptic_votes=args.skeptic_votes)


def cmd_prepare(args) -> int:
    print(summary_line(_prepare(args)))
    return 0


def cmd_verify(args) -> int:
    print(summary_line(stages.verify(args.run)))
    return 0


def cmd_recheck(args) -> int:
    print(summary_line(stages.recheck_prep(args.run)))
    return 0


def cmd_aggregate(args) -> int:
    print(summary_line(stages.aggregate_stage(args.run)))
    return 0


def cmd_report(args) -> int:
    from .report import build_report
    rep = build_report(args.run, runner=args.runner, backend=args.backend, model=args.model, fixture=args.fixture)
    print(summary_line({"stage": "report", "findings": len(rep["findings"]), "killed": len(rep["killed"]),
                        "report": str(Path(args.run) / "report.md")}))
    return 0


def cmd_validate(args) -> int:
    from .schemas import validate_role_output
    try:
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: cannot read JSON: {exc}")
        return 1
    errors = validate_role_output(args.role, data)
    if errors:
        print("INVALID:")
        for e in errors[:20]:
            print(f"  {e}")
        return 1
    print("OK")
    return 0


def cmd_fake_agent(args) -> int:
    from .llm.fake import FakeBackend
    from .roles import build_request
    from .runstore import Run
    from .schemas import validate_role_output
    run = Run(args.run)
    req = build_request(run, args.role, args.label, args.input)
    data = FakeBackend().complete(req).data
    errors = validate_role_output(args.role, data)
    if errors:
        print("fake agent produced invalid output: " + "; ".join(errors[:3]), file=sys.stderr)
        return 1
    run.write_json(f"agents/{args.label}.json", data)
    n = len(data.get("findings", data.get("verdicts", data.get("ordered_finding_ids", []))))
    print(summary_line({"stage": "fake-agent", "label": args.label, "n_items": n}))
    return 0


def cmd_run(args) -> int:
    from .budget import Budget
    from .llm.base import FatalError
    from .pipeline import PythonRunner, RunnerConfig
    try:
        if args.backend == "fake":
            from .llm.fake import FakeBackend
            backend = FakeBackend()
        else:
            from .llm.anthropic_backend import AnthropicBackend
            backend = AnthropicBackend(model=args.model)
        budget = Budget(max_input_tokens=args.max_input_tokens, max_output_tokens=args.max_output_tokens,
                        max_cost_usd=args.max_cost_usd, model=backend.model)
    except FatalError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(summary_line(_prepare(args)))
    cfg = RunnerConfig(concurrency=args.concurrency, retries=args.retries, skeptic_votes=args.skeptic_votes or 1,
                       gap_reader=not args.no_gap_reader, max_tokens=args.max_tokens)
    rep = PythonRunner(args.run, backend, budget, cfg).run()
    pipe = rep["pipeline"]
    print(summary_line({"stage": "run", "findings": len(rep["findings"]), "killed": len(rep["killed"]),
                        "rejected_by_verifier": pipe["verification"]["rejected"], "usage": pipe["usage"],
                        "incomplete": pipe["incomplete"]}))
    if pipe["incomplete"]:
        # The report is still written, but a run that stopped calling the API
        # (missing credentials, cost or token cap) must not look like a success.
        print(f"error: run incomplete: {pipe['incomplete']}", file=sys.stderr)
        return 3
    return 0


def cmd_baseline(args) -> int:
    from .evaluation import baseline
    print(summary_line(baseline(args.run)))
    return 0


def cmd_score(args) -> int:
    from .evaluation import score
    result = score(args.run, args.truth, source=args.source)
    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)
    return 0


def cmd_export(args) -> int:
    from .workflow_assets import WORKFLOW_PATH, check_or_write
    ok = check_or_write(write=not args.check)
    if args.check and not ok:
        print(f"{WORKFLOW_PATH} is out of date: run python -m docaudit export-workflow-assets")
        return 1
    print("OK" if args.check else f"updated {WORKFLOW_PATH}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="docaudit", description="Quote-verified multi-agent document audit and diff.")
    ap.add_argument("--version", action="version", version=f"docaudit {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare", help="ingest, align, sweep and chunk; write the run directory")
    _add_prepare_args(p)
    p.set_defaults(fn=cmd_prepare)

    for name, fn, hlp in [("verify", cmd_verify, "quote-verify, merge and batch agent findings"),
                          ("recheck-prep", cmd_recheck, "verify the skeptics' missed findings and queue a recheck"),
                          ("aggregate", cmd_aggregate, "apply skeptic verdicts: severity and confidence")]:
        p = sub.add_parser(name, help=hlp)
        p.add_argument("--run", required=True)
        p.set_defaults(fn=fn)

    p = sub.add_parser("report", help="write report.md and report.json")
    p.add_argument("--run", required=True)
    p.add_argument("--runner", default="workflow")
    p.add_argument("--backend", default="claude-code")
    p.add_argument("--model")
    p.add_argument("--fixture", action="store_true", help="label the report as a fixture run")
    p.set_defaults(fn=cmd_report)

    p = sub.add_parser("validate", help="validate an agent output file against its role schema")
    p.add_argument("--role", required=True, choices=["section_reader", "cross_reference_checker", "gap_reader", "skeptic", "editor"])
    p.add_argument("file")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("run", help="prepare and run the whole pipeline with the Python runner")
    _add_prepare_args(p)
    p.add_argument("--backend", choices=["fake", "anthropic"], default="fake")
    p.add_argument("--model", help="model id (default: DOCAUDIT_MODEL)")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--max-tokens", type=int, default=16000, help="max_tokens per call (doubled on truncation, up to 64000)")
    p.add_argument("--max-cost-usd", type=float)
    p.add_argument("--max-input-tokens", type=int)
    p.add_argument("--max-output-tokens", type=int)
    p.add_argument("--no-gap-reader", action="store_true")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("fake-agent", help="run one FakeLLM agent call (offline workflow test)")
    p.add_argument("--run", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--input", required=True, help="input file relative to the run directory")
    p.set_defaults(fn=cmd_fake_agent)

    p = sub.add_parser("baseline", help="deterministic no-LLM baseline findings")
    p.add_argument("--run", required=True)
    p.set_defaults(fn=cmd_baseline)

    p = sub.add_parser("score", help="score a run against ground truth")
    p.add_argument("--run", required=True)
    p.add_argument("--truth", required=True)
    p.add_argument("--source", choices=["final", "baseline"], default="final")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("export-workflow-assets", help="sync schemas and role prompts into the workflow script")
    p.add_argument("--check", action="store_true")
    p.set_defaults(fn=cmd_export)

    args = ap.parse_args(argv)
    return args.fn(args)
