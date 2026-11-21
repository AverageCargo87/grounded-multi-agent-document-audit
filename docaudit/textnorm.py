"""Text normalisation shared by ingest, alignment and the quote verifier.

Three levels are used throughout the project:

* ``collapse_ws``: whitespace only. A quote that matches at this level is an
  "exact" match (LLMs routinely re-wrap lines, which is never a fabrication).
* ``normalize_loose``: Unicode NFKC, typographic quotes and dashes folded to
  ASCII, soft hyphens and hyphenation removed, light Markdown emphasis
  stripped, case folded. A quote that only matches here is a "normalized"
  match and is reported as such.
* ``tokens``: word tokens of the loose form, used for similarity scores.

Every typographic character is written as an escape so the source stays ASCII.
"""

from __future__ import annotations

import re
import unicodedata

_SINGLE_QUOTES = "\u2018\u2019\u201a\u201b\u2032\u00b4"
_DOUBLE_QUOTES = "\u201c\u201d\u201e\u201f\u2033\u00ab\u00bb"
_DASHES = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe58\ufe63\uff0d"

_TRANSLATION: dict[int, str] = {}
for _ch in _SINGLE_QUOTES:
    _TRANSLATION[ord(_ch)] = "'"
for _ch in _DOUBLE_QUOTES:
    _TRANSLATION[ord(_ch)] = '"'
for _ch in _DASHES:
    _TRANSLATION[ord(_ch)] = "-"
_TRANSLATION[ord("\u00a0")] = " "
_TRANSLATION[ord("\u2026")] = "..."
_TRANSLATION[ord("\u00ad")] = ""

_WS_RE = re.compile(r"\s+")
_EMPHASIS_RE = re.compile(r"\*\*|__|`")
# A hyphen directly after a word character and before a word character, with
# optional whitespace after it: covers "non-exclusive", "Mate- rial" (a PDF
# line-break hyphen after joining) and "Mate-\nrial".
_INTRAWORD_HYPHEN_RE = re.compile(r"(?<=\w)-\s*(?=\w)")
_TOKEN_RE = re.compile(r"\w+")
ELLIPSIS_RE = re.compile(r"\.\.\.|\u2026|\[\.\.\.\]|\[\u2026\]")


def collapse_ws(text: str) -> str:
    """Collapse every whitespace run to one space and strip the ends."""
    return _WS_RE.sub(" ", text).strip()


def fold_typography(text: str) -> str:
    """NFKC plus ASCII folding of quotes, dashes, ellipsis and odd spaces."""
    return unicodedata.normalize("NFKC", text).translate(_TRANSLATION)


def normalize_loose(text: str) -> str:
    """The comparison form used for 'normalized' quote matches and fingerprints."""
    text = fold_typography(text)
    text = _EMPHASIS_RE.sub("", text)
    text = collapse_ws(text)
    text = _INTRAWORD_HYPHEN_RE.sub("", text)
    return text.casefold()


def tokens(text: str) -> list[str]:
    """Word tokens of the loose form."""
    return _TOKEN_RE.findall(normalize_loose(text))


def word_count(text: str) -> int:
    return len(_TOKEN_RE.findall(text))


def split_ellipsis(quote: str) -> list[str]:
    """Split a quote on ellipsis markers; returns stripped non-empty segments."""
    return [seg.strip() for seg in ELLIPSIS_RE.split(quote) if seg.strip()]
