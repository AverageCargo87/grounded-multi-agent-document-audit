"""JSON schemas for every agent role, plus a small validator.

The schemas use only the JSON Schema subset that the Messages API accepts for
structured outputs (no numeric or length constraints, ``additionalProperties:
false`` on every object, every property required). Ranges such as
``0 <= confidence <= 1`` are enforced in code by the verifier.

The Claude Code Workflow script embeds an exported copy of these schemas
(``python -m docaudit export-workflow-assets``); a test fails if they drift.
"""

from __future__ import annotations

import copy

SEVERITIES = ["critical", "major", "minor", "info"]
DIFF_KINDS = ["added", "removed", "changed", "moved"]
DEFECT_KINDS = ["contradiction", "inconsistent_value", "broken_reference", "undefined_term", "ambiguity", "omission", "other"]
ALL_KINDS = DIFF_KINDS + DEFECT_KINDS

KINDS_BY_MODE = {
    "audit": DEFECT_KINDS,
    "diff": DIFF_KINDS + ["broken_reference", "contradiction", "inconsistent_value", "omission"],
}

EVIDENCE = {
    "type": "object",
    "additionalProperties": False,
    "required": ["doc", "para_id", "quote"],
    "properties": {
        "doc": {"type": "string", "enum": ["A", "B"], "description": "Document key: A (audit target or old version) or B (new version)."},
        "para_id": {"type": "string", "description": "Paragraph id exactly as shown, for example p0042."},
        "quote": {"type": "string", "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."},
    },
}

FINDING = {
    "type": "object",
    "additionalProperties": False,
    "required": ["kind", "title", "description", "severity", "confidence", "evidence"],
    "properties": {
        "kind": {"type": "string", "enum": ALL_KINDS},
        "title": {"type": "string", "description": "One line, specific: what changed or what is wrong, and where."},
        "description": {"type": "string", "description": "Two to five sentences: the problem, why it matters, and for diff findings the before and after."},
        "severity": {"type": "string", "enum": SEVERITIES},
        "confidence": {"type": "number", "description": "0.0 to 1.0: probability that a careful reviewer accepts the finding as stated."},
        "evidence": {"type": "array", "items": EVIDENCE},
    },
}

FINDINGS_OUTPUT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["findings", "coverage_note"],
    "properties": {
        "findings": {"type": "array", "items": FINDING},
        "coverage_note": {"type": "string", "description": "What you checked, what you could not judge, and which changes you judged editorial (by op number or paragraph id)."},
    },
}

VERDICT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["finding_id", "verdict", "reason", "suggested_severity", "counter_evidence"],
    "properties": {
        "finding_id": {"type": "string", "description": "Id of the finding under review, for example F007."},
        "verdict": {"type": "string", "enum": ["upheld", "weakened", "refuted"]},
        "reason": {"type": "string", "description": "What you checked and why the verdict follows."},
        "suggested_severity": {"type": "string", "enum": SEVERITIES + ["keep"]},
        "counter_evidence": {"type": "array", "items": EVIDENCE, "description": "Verbatim quotes that support a refuted or weakened verdict."},
    },
}

SKEPTIC_OUTPUT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["verdicts", "missed"],
    "properties": {
        "verdicts": {"type": "array", "items": VERDICT},
        "missed": {"type": "array", "items": FINDING, "description": "Substantive issues in the cited sections that no listed finding covers."},
    },
}

EDITOR_OUTPUT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["executive_summary", "themes", "ordered_finding_ids"],
    "properties": {
        "executive_summary": {"type": "string"},
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "finding_ids"],
                "properties": {"title": {"type": "string"}, "finding_ids": {"type": "array", "items": {"type": "string"}}},
            },
        },
        "ordered_finding_ids": {"type": "array", "items": {"type": "string"}},
    },
}

ROLE_SCHEMAS = {
    "section_reader": FINDINGS_OUTPUT,
    "cross_reference_checker": FINDINGS_OUTPUT,
    "gap_reader": FINDINGS_OUTPUT,
    "skeptic": SKEPTIC_OUTPUT,
    "editor": EDITOR_OUTPUT,
}

# Workflow-only envelopes: what a workflow subagent returns to the script.
RECEIPT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["output_path", "valid", "n_items"],
    "properties": {
        "output_path": {"type": "string"},
        "valid": {"type": "boolean", "description": "True only if the docaudit validate command printed OK for the file."},
        "n_items": {"type": "integer", "description": "Number of findings (or verdicts) written."},
    },
}

SHELL_RESULT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["exit_code", "summary_json"],
    "properties": {
        "exit_code": {"type": "integer"},
        "summary_json": {"type": "string", "description": "The last stdout line, copied exactly (it is a JSON object)."},
    },
}


def schema_for(role: str) -> dict:
    return copy.deepcopy(ROLE_SCHEMAS[role])


# ---------------------------------------------------------------- validator

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value, t: str) -> bool:
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[t])


def validate(value, schema: dict, path: str = "$") -> list[str]:
    """Validate against the schema subset used in this project. Returns errors."""
    errors: list[str] = []
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_type_ok(value, x) for x in types):
            return [f"{path}: expected {t}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property '{key}'")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}: unexpected property '{key}'")
        for key, sub in props.items():
            if key in value:
                errors.extend(validate(value[key], sub, f"{path}.{key}"))
    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            errors.extend(validate(item, schema["items"], f"{path}[{i}]"))
    return errors


def validate_role_output(role: str, value) -> list[str]:
    return validate(value, ROLE_SCHEMAS[role])
