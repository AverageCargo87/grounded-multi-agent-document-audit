"""Build the planted evaluation fixture from the CC BY 4.0 legal code.

Reads  examples/planted/cc-by-4.0.txt          (verbatim CC BY 4.0 legal code; its text is CC0)
Writes examples/planted/cc-by-4.0-planted.txt  (the copy with planted changes)
       examples/planted/ground_truth.json      (one item per planted change)

Every planted change is declared once below, together with its ground-truth
metadata, so the fixture and the truth file cannot drift apart. The script is
deterministic; ``--check`` verifies that the committed files are up to date.

Usage: python scripts/make_planted.py [--check]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "examples" / "planted" / "cc-by-4.0.txt"
PLANTED = ROOT / "examples" / "planted" / "cc-by-4.0-planted.txt"
TRUTH = ROOT / "examples" / "planted" / "ground_truth.json"

BANNER = (
    "EVALUATION FIXTURE. This file is a deliberately modified copy of the\n"
    "Creative Commons Attribution 4.0 International legal code, made to test\n"
    "document comparison tools. It is not a Creative Commons license and must\n"
    "not be used as one. The planted changes are listed in ground_truth.json.\n\n"
)

# op: replace | delete_block | insert_after_block | move_block | rewrap_block | prepend
EDITS = [
    {"id": "X00", "op": "prepend", "new": BANNER, "category": "fixture_banner", "substantive": False, "ignore": True,
     "modes": ["diff"], "description": "Fixture banner added at the top (expected, not scored).",
     "anchors_b": ["EVALUATION FIXTURE. This file is a deliberately modified copy"]},
    {"id": "P01", "op": "replace", "old": "cured within 30 days of Your discovery", "new": "cured within 60 days of Your discovery",
     "category": "changed_value", "substantive": True, "modes": ["diff"],
     "description": "Cure period for automatic reinstatement doubled from 30 to 60 days (Section 6(b)(1)).",
     "anchors_a": ["cured within 30 days"], "anchors_b": ["cured within 60 days"]},
    {"id": "P02", "op": "replace", "old": "No downstream restrictions. You may not offer or impose",
     "new": "No downstream restrictions. You may offer or impose", "category": "changed_permission", "substantive": True,
     "modes": ["diff"], "description": "Prohibition on imposing additional terms on recipients turned into a permission (Section 2(a)(5)(B)).",
     "anchors_a": ["You may not offer or impose"], "anchors_b": ["You may offer or impose"]},
    {"id": "P03", "op": "delete_block",
     "old": "3. If requested by the Licensor, You must remove any of the information required by Section 3(a)(1)(A) to the extent reasonably practicable.",
     "category": "removed_clause", "substantive": True, "modes": ["diff", "audit"],
     "description": "Section 3(a)(3) (removal of attribution on request) deleted; the list now jumps from 2 to 4.",
     "anchors_a": ["If requested by the Licensor, You must remove any of the"],
     "anchors_b": ["4. If You Share Adapted Material You produce"],
     "audit_anchors": ["4. If You Share Adapted Material You produce", "2. You may satisfy the conditions in Section 3(a)(1)"],
     "audit_kinds": ["omission", "inconsistent_value", "other"]},
    {"id": "P04", "op": "insert_after_block",
     "anchor": "Material from complying with this Public License.",
     "new": "       5. If You Share the Licensed Material for commercial purposes,\n          You must notify the Licensor in writing at least 10 days in\n          advance.",
     "category": "added_obligation", "substantive": True, "modes": ["diff"],
     "description": "New Section 3(a)(5): advance written notice before commercial sharing.",
     "anchors_b": ["You must notify the Licensor in writing at least 10 days"]},
    {"id": "P05", "op": "replace", "old": "non-exclusive, irrevocable license to", "new": "non-exclusive, revocable license to",
     "category": "changed_grant", "substantive": True, "modes": ["diff"],
     "description": "License grant changed from irrevocable to revocable (Section 2(a)(1)).",
     "anchors_a": ["non-exclusive, irrevocable license"], "anchors_b": ["non-exclusive, revocable license"]},
    {"id": "P06", "op": "replace",
     "old": "The Licensor shall not be bound by any additional or different terms or conditions communicated by You unless expressly agreed.",
     "new": "You shall not be bound by any additional or different\n     terms or conditions communicated by the Licensor unless expressly agreed.",
     "category": "changed_party", "substantive": True, "modes": ["diff"],
     "description": "Parties swapped in Section 7(a): the licensee, not the Licensor, is protected from additional terms.",
     "anchors_a": ["The Licensor shall not be bound by any additional"], "anchors_b": ["You shall not be bound by any additional"]},
    {"id": "P07", "op": "replace", "old": "has terminated under Section 6(a), it reinstates:",
     "new": "has terminated under\n     Section 9(a), it reinstates:",
     "category": "broken_reference", "substantive": True, "modes": ["diff", "audit"],
     "description": "Reference in Section 6(b) changed to Section 9(a), which does not exist.",
     "anchors_a": ["terminated under Section 6(a), it reinstates"], "anchors_b": ["terminated under Section 9(a), it reinstates"],
     "audit_anchors": ["terminated under Section 9(a), it reinstates"], "audit_kinds": ["broken_reference", "other"]},
    {"id": "P08", "op": "replace", "old": "translated, altered, arranged, transformed, or otherwise modified in a manner requiring",
     "new": "translated or altered in a manner requiring",
     "category": "changed_definition", "substantive": True, "modes": ["diff"],
     "description": "Definition of Adapted Material narrowed: 'arranged, transformed, or otherwise modified' dropped (Section 1(a)).",
     "anchors_a": ["arranged, transformed, or otherwise modified"], "anchors_b": ["Licensed Material is translated or altered in a manner requiring"]},
    {"id": "P09", "op": "replace", "old": "c. You must comply with the conditions in Section 3(a) if You Share",
     "new": "c. You should comply with the conditions in Section 3(a) if You Share",
     "category": "weakened_obligation", "substantive": True, "modes": ["diff"],
     "description": "Obligation in Section 4(c) weakened from 'must' to 'should'.",
     "anchors_a": ["You must comply with the conditions in Section 3(a)"], "anchors_b": ["You should comply with the conditions in Section 3(a)"]},
    {"id": "P10", "op": "replace", "old": "Sections 1, 5, 6, 7, and 8 survive termination", "new": "Sections 1, 5, 7, and 8 survive termination",
     "category": "changed_value", "substantive": True, "modes": ["diff"],
     "description": "Section 6 dropped from the list of sections that survive termination (Section 6(d)).",
     "anchors_a": ["Sections 1, 5, 6, 7, and 8 survive"], "anchors_b": ["Sections 1, 5, 7, and 8 survive"]},
    {"id": "P11", "op": "replace", "old": "3. Term. The term of this Public License is specified in Section 6(a).",
     "new": "3. Term. The term of this Public License is five years from the\n          date You accept it.",
     "category": "contradiction", "substantive": True, "modes": ["diff", "audit"],
     "description": "Section 2(a)(3) now sets a five-year term, contradicting Section 6(a) (term of the Copyright and Similar Rights).",
     "anchors_a": ["The term of this Public License is specified in Section"], "anchors_b": ["The term of this Public License is five years"],
     "audit_anchors": ["The term of this Public License is five years", "This Public License applies for the term of the Copyright"],
     "audit_kinds": ["contradiction", "inconsistent_value", "ambiguity", "other"]},
    {"id": "P12", "op": "move_block",
     "old": "d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You, including from the legal processes of any jurisdiction or authority.",
     "anchor": "independent of the terms and conditions of this Public License.", "relabel": ["d.", "c."],
     "category": "moved_clause", "substantive": True, "modes": ["diff"],
     "description": "Privileges-and-immunities clause moved from Section 8(d) to Section 7(c).",
     "anchors_a": ["privileges and immunities that apply to the Licensor or You"],
     "anchors_b": ["privileges and immunities that apply to the Licensor or You"]},
    {"id": "P13", "op": "replace", "old": "authorizes You to exercise the Licensed Rights in all media",
     "new": "authorizes You to exercise the Granted Rights in\n          all media",
     "category": "undefined_term", "substantive": True, "modes": ["diff", "audit"],
     "description": "Section 2(a)(4) now uses 'Granted Rights', a term that is never defined.",
     "anchors_a": ["authorizes You to exercise the Licensed Rights in all media"],
     "anchors_b": ["authorizes You to exercise the Granted Rights in all media"],
     "audit_anchors": ["authorizes You to exercise the Granted Rights in all media"],
     "audit_kinds": ["undefined_term", "ambiguity", "other"]},
    {"id": "E01", "op": "replace", "old": "Patent and trademark rights are not licensed under this Public License.",
     "new": "Patent and trademark rights are not licenced under this\n          Public Licence.",
     "category": "spelling_variant", "substantive": False, "modes": ["diff"],
     "description": "British spelling 'licenced' / 'Licence' in Section 2(b)(2). Editorial.",
     "anchors_a": ["Patent and trademark rights are not licensed"], "anchors_b": ["Patent and trademark rights are not licenced"]},
    {"id": "E02", "op": "rewrap_block", "old": "b. To the extent possible, if any provision of this Public License is deemed unenforceable",
     "category": "rewrap", "substantive": False, "modes": ["diff"],
     "description": "Section 8(b) re-wrapped at a different line width. Whitespace only.",
     "anchors_a": ["deemed unenforceable, it shall be automatically reformed"],
     "anchors_b": ["deemed unenforceable, it shall be automatically reformed"]},
    {"id": "E03", "op": "replace", "old": "(\"Public License\")", "new": "(\u201cPublic License\u201d)",
     "category": "typography", "substantive": False, "modes": ["diff"],
     "description": "Straight quotes replaced by typographic quotes in the preamble. Editorial.",
     "anchors_a": ["By exercising the Licensed Rights (defined below)"], "anchors_b": ["By exercising the Licensed Rights (defined below)"]},
    {"id": "E04", "op": "replace", "old": "dissemination, communication, or importation", "new": "dissemination,\n     communication or importation",
     "category": "punctuation", "substantive": False, "modes": ["diff"],
     "description": "Serial comma removed in the definition of Share (Section 1(i)). Editorial.",
     "anchors_a": ["communication, or importation"], "anchors_b": ["communication or importation"]},
    {"id": "E05", "op": "replace", "old": "as well as other essentially equivalent rights", "new": "as well as other essen-\n     tially equivalent rights",
     "category": "hyphenation", "substantive": False, "modes": ["diff"],
     "description": "Line-break hyphenation inside 'essentially' (Section 1(j)). Editorial.",
     "anchors_a": ["Directive 96/9/EC of the European Parliament"], "anchors_b": ["Directive 96/9/EC of the European Parliament"]},
]


def _flex(text: str) -> re.Pattern:
    """Regex matching ``text`` with any whitespace run matching any whitespace run."""
    parts = [re.escape(p) for p in text.split()]
    return re.compile(r"\s+".join(parts))


def _find_once(text: str, needle: str) -> re.Match:
    hits = list(_flex(needle).finditer(text))
    if len(hits) != 1:
        raise SystemExit(f"edit target {needle[:60]!r} matches {len(hits)} times; it must match exactly once")
    return hits[0]


def _block_span(text: str, m: re.Match) -> tuple[int, int]:
    """Expand a match to its whole paragraph (up to the next blank line) plus the blank lines after it."""
    start = text.rfind("\n", 0, m.start()) + 1
    blank = re.compile(r"\n[ \t]*\n")
    b = blank.search(text, m.end())
    end = len(text) if b is None else b.start() + 1
    while end < len(text) and text[end] == "\n":
        end += 1
    return start, end


def apply_edits(base: str) -> str:
    text = base
    for e in EDITS:
        op = e["op"]
        if op == "prepend":
            text = e["new"] + text
        elif op == "replace":
            m = _find_once(text, e["old"])
            text = text[: m.start()] + e["new"] + text[m.end():]
        elif op == "delete_block":
            m = _find_once(text, e["old"])
            s, t = _block_span(text, m)
            text = text[:s] + text[t:]
        elif op == "insert_after_block":
            m = _find_once(text, e["anchor"])
            _, t = _block_span(text, m)
            text = text[:t] + e["new"] + "\n\n" + text[t:]
        elif op == "move_block":
            m = _find_once(text, e["old"])
            s, t = _block_span(text, m)
            block = text[s:t].rstrip("\n")
            old_label, new_label = e["relabel"]
            block = block.replace(old_label, new_label, 1)
            text = text[:s] + text[t:]
            a = _find_once(text, e["anchor"])
            _, t2 = _block_span(text, a)
            text = text[:t2] + block + "\n\n" + text[t2:]
        elif op == "rewrap_block":
            m = _find_once(text, e["old"])
            s, t = _block_span(text, m)
            block = text[s:t].rstrip("\n")
            indent = len(block) - len(block.lstrip(" "))
            words = " ".join(block.split())
            wrapped = textwrap.fill(words, width=58, initial_indent=" " * indent, subsequent_indent=" " * (indent + 3))
            text = text[:s] + wrapped + "\n\n" + text[t:]
        else:
            raise SystemExit(f"unknown op {op}")
    return text


def truth() -> dict:
    keys = ["id", "category", "substantive", "modes", "description", "anchors_a", "anchors_b", "audit_anchors", "audit_kinds", "ignore"]
    items = []
    for e in EDITS:
        item = {k: e[k] for k in keys if k in e}
        item.setdefault("ignore", False)
        items.append(item)
    return {
        "description": "Planted changes between the CC BY 4.0 legal code (A) and an evaluation copy (B). "
                       "Diff mode compares A with B; audit mode audits B alone against the audit_anchors items.",
        "base": "examples/planted/cc-by-4.0.txt",
        "fixture": "examples/planted/cc-by-4.0-planted.txt",
        "generator": "scripts/make_planted.py",
        "items": items,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if the committed files differ from a fresh build")
    args = ap.parse_args()
    base = BASE.read_text(encoding="utf-8")
    planted = apply_edits(base)
    truth_text = json.dumps(truth(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        ok = PLANTED.read_text(encoding="utf-8") == planted and TRUTH.read_text(encoding="utf-8") == truth_text
        print("OK" if ok else "OUT OF DATE")
        return 0 if ok else 1
    PLANTED.write_text(planted, encoding="utf-8", newline="\n")
    TRUTH.write_text(truth_text, encoding="utf-8", newline="\n")
    print(f"wrote {PLANTED.relative_to(ROOT)} and {TRUTH.relative_to(ROOT)} ({len(EDITS)} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
