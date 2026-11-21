"""Keep the Workflow script's schemas and role prompts identical to the Python ones.

The script cannot import Python or read files, so the generated block between
the markers below holds a JSON copy of ``schemas.py`` and ``prompts.py``.
``python -m docaudit export-workflow-assets`` rewrites it; ``--check`` (and a
test) fails when it is stale.
"""

from __future__ import annotations

import json
from pathlib import Path

from .prompts import all_role_systems
from .schemas import RECEIPT, ROLE_SCHEMAS, SHELL_RESULT

WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "workflow" / "document-audit.workflow.js"
START = "// <generated:workflow-assets>"
END = "// </generated:workflow-assets>"


def render_block() -> str:
    schemas = {"roles": ROLE_SCHEMAS, "receipt": RECEIPT, "shell": SHELL_RESULT}
    return (
        f"{START}\n"
        "// Generated from docaudit/schemas.py and docaudit/prompts.py by\n"
        "// `python -m docaudit export-workflow-assets`. Do not edit by hand.\n"
        f"const SCHEMAS = {json.dumps(schemas, indent=2)}\n"
        f"const ROLE_SYSTEM = {json.dumps(all_role_systems(), indent=2)}\n"
        f"{END}"
    )


def check_or_write(write: bool = True, path: Path = WORKFLOW_PATH) -> bool:
    text = path.read_text(encoding="utf-8")
    start = text.index(START)
    end = text.index(END) + len(END)
    fresh = text[:start] + render_block() + text[end:]
    if fresh == text:
        return True
    if write:
        path.write_text(fresh, encoding="utf-8", newline="\n")
    return False
