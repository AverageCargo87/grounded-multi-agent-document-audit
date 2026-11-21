"""The run directory: the file contract shared by both runners.

    runs/<name>/
      plan.json             mode, documents, chunks, configuration
      docs/A.json, B.json   ingested documents (paragraph ids, text, sections)
      docs/A.md, B.md       numbered rendering that agents read and quote from
      alignment.json        diff mode only
      sweeps.json           deterministic sweep findings
      index.md              cross-reference checker input
      chunks/cNN.md         section reader inputs
      agents/*.json         agent outputs (THE contract between runners and core)
      verified.json         after quote verification, merge and coverage
      gaps.md               diff mode: changes no accepted finding cites
      skeptic/bNN.json|.md  skeptic inputs
      verified_missed.json  findings the skeptics reported as missed
      skeptic/r01.json|.md  recheck input
      aggregated.json       after skeptic verdicts
      editor_input.md       editor input
      report.md, report.json
      usage.json            Python runner only: calls, tokens, cost

Agent output files are named by role:
reader-<chunk>.json, crossref.json, gap.json, skeptic-<batch>-v<k>.json,
recheck-<batch>-v<k>.json, editor.json.
"""

from __future__ import annotations

import json
from functools import cached_property
from pathlib import Path

from .align import Alignment
from .ingest import Document


def dump_json(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


class Run:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def path(self, rel: str) -> Path:
        return self.root / rel

    def exists(self, rel: str) -> bool:
        return self.path(rel).exists()

    def write_json(self, rel: str, obj) -> Path:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(dump_json(obj), encoding="utf-8", newline="\n")
        return p

    def write_text(self, rel: str, text: str) -> Path:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        return p

    def read_json(self, rel: str):
        return json.loads(self.path(rel).read_text(encoding="utf-8"))

    def read_text(self, rel: str) -> str:
        return self.path(rel).read_text(encoding="utf-8")

    @cached_property
    def plan(self) -> dict:
        return self.read_json("plan.json")

    @property
    def mode(self) -> str:
        return self.plan["mode"]

    @cached_property
    def docs(self) -> dict[str, Document]:
        keys = ["A", "B"] if self.mode == "diff" else ["A"]
        return {k: Document.from_dict(self.read_json(f"docs/{k}.json")) for k in keys}

    @cached_property
    def alignment(self) -> Alignment | None:
        if self.mode != "diff":
            return None
        return Alignment.from_dict(self.read_json("alignment.json"))

    def agent_files(self, pattern: str) -> list[Path]:
        return sorted(self.path("agents").glob(pattern))

    def agent_outputs(self, pattern: str) -> list[tuple[str, dict]]:
        out = []
        for p in self.agent_files(pattern):
            try:
                out.append((p.stem, json.loads(p.read_text(encoding="utf-8"))))
            except json.JSONDecodeError as exc:
                out.append((p.stem, {"_error": f"invalid JSON: {exc}"}))
        return out
