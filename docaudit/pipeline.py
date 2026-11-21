"""The Python runner: drives the agent roles through a Backend, with bounded
concurrency, retries with exponential backoff, and token and cost caps.

It writes exactly the files the Claude Code Workflow script writes
(``agents/*.json``), and calls the same deterministic stages, so the core
cannot tell which runner produced a run directory.
"""

from __future__ import annotations

import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import stages
from .budget import Budget
from .llm.base import AuthError, Backend, BudgetExceeded, FatalError, LLMRequest, RetryableError
from .report import build_report
from .roles import OUTPUT_PREFIX, build_request
from .runstore import Run
from .schemas import validate_role_output


@dataclass
class RunnerConfig:
    concurrency: int = 4
    retries: int = 3
    base_delay: float = 2.0
    max_delay: float = 60.0
    max_tokens: int = 16000
    max_tokens_ceiling: int = 64000
    skeptic_votes: int = 1
    gap_reader: bool = True


class PythonRunner:
    def __init__(self, run_dir: str | Path, backend: Backend, budget: Budget | None = None,
                 config: RunnerConfig | None = None, sleep: Callable[[float], None] = time.sleep,
                 log: Callable[[str], None] = print) -> None:
        self.run_dir = Path(run_dir)
        self.backend = backend
        self.budget = budget or Budget(model=getattr(backend, "model", None))
        self.cfg = config or RunnerConfig()
        self.sleep = sleep
        self.log = log
        self.calls: list[dict] = []
        self.failures: list[dict] = []
        self.incomplete: str | None = None
        self.lock = threading.Lock()

    # ------------------------------------------------------------ one call

    def _delay(self, attempt: int, label: str) -> float:
        jitter = random.Random(f"{label}:{attempt}").uniform(0, 0.5)
        return min(self.cfg.max_delay, self.cfg.base_delay * (2 ** attempt) + jitter)

    def call(self, role: str, label: str, input_rel: str) -> bool:
        run = Run(self.run_dir)
        if self.incomplete:
            self._fail(label, f"skipped: {self.incomplete}")
            return False
        req = build_request(run, role, label, input_rel)
        req.max_tokens = self.cfg.max_tokens
        est_in = (len(req.system) + len(req.prompt) + len(req.prefix or "")) // 4
        record = {"label": label, "role": role, "attempts": 0, "input_tokens": 0, "output_tokens": 0,
                  "cache_read_tokens": 0, "cache_write_tokens": 0, "cost_usd": 0.0, "ok": False, "error": None}
        last_error: Exception | None = None
        attempt_req = req
        for attempt in range(self.cfg.retries + 1):
            record["attempts"] = attempt + 1
            try:
                reservation = self.budget.reserve(est_in)
            except BudgetExceeded as exc:
                with self.lock:
                    self.incomplete = self.incomplete or f"budget cap reached before {label}: {exc}"
                record["error"] = f"budget: {exc}"
                self._fail(label, record["error"], record)
                return False
            try:
                resp = self.backend.complete(attempt_req)
            except RetryableError as exc:
                self.budget.release(reservation)
                last_error = exc
                if type(exc).__name__ == "MaxTokensError":
                    attempt_req = _replace(attempt_req, max_tokens=min(self.cfg.max_tokens_ceiling, attempt_req.max_tokens * 2))
                if attempt < self.cfg.retries:
                    self.sleep(self._delay(attempt, label))
                continue
            except (FatalError, Exception) as exc:  # noqa: BLE001 - recorded, never swallowed silently
                self.budget.release(reservation)
                record["error"] = f"{type(exc).__name__}: {exc}"
                if isinstance(exc, AuthError):
                    with self.lock:
                        self.incomplete = self.incomplete or f"stopped calling the API: {exc}"
                self._fail(label, record["error"], record)
                return False
            cost = self.budget.commit(reservation, resp.usage)
            for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens"):
                record[k] += getattr(resp.usage, k)
            record["cost_usd"] = round(record["cost_usd"] + cost, 6)
            errors = validate_role_output(role, resp.data)
            if errors:
                last_error = RetryableError("schema: " + "; ".join(errors[:3]))
                # Keep any max_tokens increase from an earlier truncated attempt.
                attempt_req = _replace(attempt_req, prompt=req.prompt + "\n\nYour previous answer failed validation: "
                                       + "; ".join(errors[:5]) + ". Answer again with valid JSON.")
                if attempt < self.cfg.retries:
                    self.sleep(self._delay(attempt, label))
                continue
            run.write_json(f"agents/{label}.json", resp.data)
            record["ok"] = True
            with self.lock:
                self.calls.append(record)
            return True
        record["error"] = f"gave up after {record['attempts']} attempt(s): {last_error}"
        self._fail(label, record["error"], record)
        return False

    def _fail(self, label: str, error: str, record: dict | None = None) -> None:
        with self.lock:
            self.failures.append({"agent": label, "error": error})
            if record is not None:
                self.calls.append(record)
        self.log(f"  ! {label}: {error}")

    def run_tasks(self, tasks: list[tuple[str, str, str]]) -> None:
        if not tasks:
            return
        with ThreadPoolExecutor(max_workers=max(1, self.cfg.concurrency)) as pool:
            list(pool.map(lambda t: self.call(*t), tasks))

    # ------------------------------------------------------------ whole run

    def run(self) -> dict:
        run = Run(self.run_dir)
        plan = run.plan
        t0 = time.time()
        self.log(f"[1/6] section readers x{len(plan['chunks'])} + cross-reference checker")
        tasks = [("section_reader", f"{OUTPUT_PREFIX['section_reader']}-{c['id']}", c["file"]) for c in plan["chunks"]]
        tasks.append(("cross_reference_checker", "crossref", "index.md"))
        self.run_tasks(tasks)
        s = stages.verify(self.run_dir)
        self.log(f"      verify: {s}")
        if plan["mode"] == "diff" and self.cfg.gap_reader and s["uncovered"] and not self.incomplete:
            self.log(f"[2/6] gap reader on {s['uncovered']} uncovered operations")
            self.run_tasks([("gap_reader", "gap", "gaps.md")])
            s = stages.verify(self.run_dir)
            self.log(f"      verify: {s}")
        else:
            self.log("[2/6] gap reader not needed")
        tasks = []
        for b in s["batches"]:
            if not run.read_json(f"skeptic/{b}.json")["finding_ids"]:
                continue
            for k in range(1, self.cfg.skeptic_votes + 1):
                tasks.append(("skeptic", f"skeptic-{b}-v{k}", f"skeptic/{b}.md"))
        self.log(f"[3/6] skeptics x{len(tasks)}")
        self.run_tasks(tasks)
        r = stages.recheck_prep(self.run_dir)
        self.log(f"[4/6] recheck: {r}")
        if r["recheck_findings"]:
            self.run_tasks([("skeptic", f"recheck-r01-v{k}", "skeptic/r01.md") for k in range(1, self.cfg.skeptic_votes + 1)])
        a = stages.aggregate_stage(self.run_dir)
        self.log(f"[5/6] aggregate: {a}")
        self.run_tasks([("editor", "editor", "editor_input.md")])
        self.calls.sort(key=lambda c: c["label"])
        run.write_json("usage.json", {"calls": self.calls, "totals": self.budget.totals()})
        run.write_json("run_log.json", {"failures": sorted(self.failures, key=lambda f: f["agent"]), "incomplete": self.incomplete})
        report = build_report(self.run_dir, runner="python", backend=self.backend.name,
                              model=getattr(self.backend, "model", None), fixture=self.backend.name == "fake")
        self.log(f"[6/6] report: {self.run_dir / 'report.md'} ({time.time() - t0:.1f}s)")
        return report


def _replace(req: LLMRequest, **changes) -> LLMRequest:
    data = dict(req.__dict__)
    data.update(changes)
    return LLMRequest(**data)
