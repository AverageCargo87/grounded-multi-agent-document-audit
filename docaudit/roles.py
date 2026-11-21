"""Build the request for one agent call from the run directory.

The Python runner and the ``fake-agent`` command (used by the offline test of
the Workflow script) both go through ``build_request``, so the same run
directory produces the same agent inputs whichever runner drives it.
"""

from __future__ import annotations

import os

from .llm.base import LLMRequest
from .prompts import OUTPUT_INSTRUCTION, role_system
from .runstore import Run
from .schemas import schema_for

DEFAULT_EFFORT = {
    "section_reader": "medium",
    "cross_reference_checker": "high",
    "gap_reader": "medium",
    "skeptic": "high",
    "editor": "medium",
}

OUTPUT_PREFIX = {
    "section_reader": "reader",
    "cross_reference_checker": "crossref",
    "gap_reader": "gap",
    "skeptic": "skeptic",
    "editor": "editor",
}


def effort_for(role: str) -> str:
    return os.environ.get("DOCAUDIT_EFFORT") or DEFAULT_EFFORT[role]


def _docs_prefix(run: Run) -> str:
    parts = [run.read_text(f"docs/{k}.md") for k in run.docs]
    return "Full text of the document(s) under review, every paragraph tagged with its id:\n\n" + "\n\n".join(parts)


def _batch_findings(run: Run, batch_file: str) -> list[dict]:
    ids = run.read_json(batch_file.replace(".md", ".json"))["finding_ids"]
    pool = {f["id"]: f for f in run.read_json("verified.json")["findings"]}
    if run.exists("verified_missed.json"):
        pool.update({f["id"]: f for f in run.read_json("verified_missed.json")["findings"]})
    return [pool[i] for i in ids if i in pool]


def _all_findings(run: Run) -> list[dict]:
    out = list(run.read_json("verified.json")["findings"])
    if run.exists("verified_missed.json"):
        out += run.read_json("verified_missed.json")["findings"]
    return out


def build_request(run: Run, role: str, label: str, input_rel: str) -> LLMRequest:
    mode = run.mode
    system = role_system(role, mode)
    body = run.read_text(input_rel)
    ctx: dict = {"docs": run.docs, "alignment": run.alignment, "mode": mode, "label": label}
    prefix = None
    if role == "section_reader":
        chunk = next(c for c in run.plan["chunks"] if c["file"] == input_rel)
        ctx["chunk"] = chunk
        task = f"Review chunk {chunk['id']} and report findings."
    elif role == "cross_reference_checker":
        prefix = _docs_prefix(run)
        ctx["sweeps"] = run.read_json("sweeps.json")["findings"]
        task = "Using the documents above and the deterministic index below, report cross-section findings."
    elif role == "gap_reader":
        ctx["ops"] = run.read_json("gaps.json")["ops"] if run.exists("gaps.json") else []
        task = "Classify every listed operation; report the substantive ones as findings."
    elif role == "skeptic":
        prefix = _docs_prefix(run)
        ctx["findings"] = _batch_findings(run, input_rel)
        ctx["all_findings"] = _all_findings(run)
        task = "Try to refute every finding in this batch, then list what it missed."
    elif role == "editor":
        ctx["aggregated"] = run.read_json("aggregated.json")
        task = "Write the synthesis."
    else:
        raise ValueError(f"unknown role {role}")
    prompt = f"{body}\n\n{task}\n\n{OUTPUT_INSTRUCTION}"
    return LLMRequest(role=role, label=label, mode=mode, system=system, prompt=prompt, schema=schema_for(role),
                      prefix=prefix, context=ctx, effort=effort_for(role))
