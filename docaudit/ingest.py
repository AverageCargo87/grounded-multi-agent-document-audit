"""Ingest Markdown, plain text and PDF into numbered paragraphs with stable ids.

Paragraph ids (``p0001``, ``p0002``, ...) are a pure function of the input
bytes: the same file always yields the same ids, so agents, the verifier and
the report can all point at ``A:p0042`` and mean the same text. Each paragraph
also carries a content fingerprint (hash of its loose-normalised text) that is
independent of position and of line wrapping; alignment uses it to recognise
unchanged paragraphs between two versions.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .textnorm import collapse_ws, normalize_loose

_DECORATION_RE = re.compile(r"^\s*([=\-_*~#+])\1{2,}\s*$")
_LIST_RE = re.compile(r"^(\s*)\(?([a-z]{1,4}|\d{1,3}|[A-Z])[.)]\s+")
_NUMBERED_SECTION_RE = re.compile(r"^\s{0,3}(\d{1,2})\.\s+\S")
_NAMED_SECTION_RE = re.compile(
    r"^\s*(?:section|article|chapter|part)\s+(\d+|[IVXLC]+)\b", re.IGNORECASE
)
_MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_MD_BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d{1,3}[.)])\s+")
_TERMINAL_PUNCT = (".", ",", ";", ":")


@dataclass
class Paragraph:
    id: str
    index: int
    text: str
    kind: str  # heading | para | list_item | code
    section: str
    label: str | None
    indent: int
    line: int  # 1-based source line (page number for PDF)
    fingerprint: str

    def ref(self, doc_key: str) -> str:
        return f"{doc_key}:{self.id}"


@dataclass
class Section:
    key: str
    title: str
    number: str | None
    para_ids: list[str] = field(default_factory=list)


@dataclass
class Document:
    key: str
    source: str
    sha256: str
    format: str
    paragraphs: list[Paragraph]
    sections: list[Section]

    def __post_init__(self) -> None:
        self._by_id = {p.id: p for p in self.paragraphs}
        self._section_by_key = {s.key: s for s in self.sections}

    def para(self, pid: str) -> Paragraph | None:
        return self._by_id.get(pid)

    def section_of(self, pid: str) -> Section | None:
        p = self._by_id.get(pid)
        return self._section_by_key.get(p.section) if p else None

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "source": self.source,
            "sha256": self.sha256,
            "format": self.format,
            "paragraphs": [asdict(p) for p in self.paragraphs],
            "sections": [asdict(s) for s in self.sections],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        return cls(
            key=data["key"],
            source=data["source"],
            sha256=data["sha256"],
            format=data["format"],
            paragraphs=[Paragraph(**p) for p in data["paragraphs"]],
            sections=[Section(**s) for s in data["sections"]],
        )


def fingerprint(text: str) -> str:
    return hashlib.sha1(normalize_loose(text).encode("utf-8")).hexdigest()[:12]


def display_source(path: str | os.PathLike) -> str:
    """A path that is safe to store in outputs: relative if possible, else the file name."""
    p = Path(path)
    if not p.is_absolute():
        return p.as_posix()
    try:
        return p.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return p.name


# ---------------------------------------------------------------- blocks


@dataclass
class _Block:
    lines: list[str]
    line: int
    kind_hint: str | None = None  # "heading" | "code" from Markdown syntax


def _join_lines(lines: list[str]) -> str:
    out = ""
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if not out:
            out = line
        elif out.endswith("-") and len(out) > 1 and out[-2].isalpha() and line[:1].islower():
            out += line  # keep the hyphen; normalisation decides what it means
        else:
            out += " " + line
    return collapse_ws(out)


def _split_blank(lines: list[str], first_line: int = 1) -> list[_Block]:
    blocks: list[_Block] = []
    cur: list[str] = []
    start = first_line
    for offset, line in enumerate(lines):
        if line.strip():
            if not cur:
                start = first_line + offset
            cur.append(line)
        elif cur:
            blocks.append(_Block(cur, start))
            cur = []
    if cur:
        blocks.append(_Block(cur, start))
    return blocks


def _strip_decoration(block: _Block) -> _Block | None:
    kept = [ln for ln in block.lines if not _DECORATION_RE.match(ln)]
    if not kept:
        return None
    return _Block(kept, block.line, block.kind_hint)


def _blocks_markdown(lines: list[str]) -> list[_Block]:
    blocks: list[_Block] = []
    i = 0
    buf: list[str] = []
    buf_start = 1

    def flush() -> None:
        nonlocal buf
        if buf:
            for b in _split_blank(buf, buf_start):
                blocks.extend(_split_md_block(b))
        buf = []

    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            flush()
            start = i + 1
            code = [line]
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                code.append(lines[i])
                i += 1
            if i < len(lines):
                code.append(lines[i])
            blocks.append(_Block(code, start, "code"))
            i += 1
            buf_start = i + 1
            continue
        if not buf:
            buf_start = i + 1
        buf.append(line)
        i += 1
    flush()
    return blocks


def _split_md_block(block: _Block) -> list[_Block]:
    """Split headings and list items out of a Markdown blank-line block."""
    out: list[_Block] = []
    cur: list[str] = []
    cur_start = block.line
    for offset, line in enumerate(block.lines):
        ln = block.line + offset
        if _MD_HEADING_RE.match(line.strip()):
            if cur:
                out.append(_Block(cur, cur_start))
                cur = []
            out.append(_Block([line.strip()], ln, "heading"))
            continue
        if _MD_BULLET_RE.match(line) and cur:
            out.append(_Block(cur, cur_start))
            cur = []
        if not cur:
            cur_start = ln
        cur.append(line)
    if cur:
        out.append(_Block(cur, cur_start))
    return out


def _blocks_pdf(path: Path) -> list[_Block]:
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise RuntimeError("PDF input needs PyMuPDF (pip install pymupdf)") from exc
    blocks: list[_Block] = []
    with fitz.open(path) as pdf:
        for page_no, page in enumerate(pdf, start=1):
            for b in page.get_text("blocks", sort=True):
                if len(b) >= 7 and b[6] != 0:
                    continue  # image block
                text = b[4]
                lines = [ln for ln in text.splitlines() if ln.strip()]
                if lines:
                    blocks.append(_Block(lines, page_no))
    return blocks


# ---------------------------------------------------------------- classification


def _is_heading_line(text: str, indent: int) -> bool:
    words = text.split()
    if not words or len(words) > 12 or len(text) > 100:
        return False
    if _NAMED_SECTION_RE.match(text):
        return True
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.85 and len(letters) >= 4:
        return True
    if indent <= 3 and _NUMBERED_SECTION_RE.match(text) and len(words) <= 10:
        return True
    if _LIST_RE.match(text):
        return False
    if len(words) <= 10 and text[0].isupper() and not text.endswith(_TERMINAL_PUNCT):
        return True
    return False


def _section_number(text: str) -> str | None:
    m = _NAMED_SECTION_RE.match(text)
    if m:
        return m.group(1)
    m = _NUMBERED_SECTION_RE.match(text)
    if m:
        return m.group(1)
    return None


def build_document(key: str, source: str, sha256: str, fmt: str, blocks: list[_Block]) -> Document:
    paragraphs: list[Paragraph] = []
    sections: list[Section] = [Section(key="s00", title="(front matter)", number=None)]

    def new_section(title: str, number: str | None) -> Section:
        sec = Section(key=f"s{len(sections):02d}", title=title, number=number)
        sections.append(sec)
        return sec

    for block in blocks:
        cleaned = _strip_decoration(block) if block.kind_hint != "code" else block
        if cleaned is None:
            continue
        first = cleaned.lines[0].expandtabs(8)
        indent = len(first) - len(first.lstrip(" "))
        if cleaned.kind_hint == "code":
            text = "\n".join(cleaned.lines)
        else:
            text = _join_lines([ln.expandtabs(8) for ln in cleaned.lines])
        if not text:
            continue
        kind = "para"
        label = None
        section = sections[-1]
        if cleaned.kind_hint == "heading":
            m = _MD_HEADING_RE.match(text)
            title = m.group(2).strip() if m else text
            kind = "heading"
            section = new_section(title, _section_number(title))
        elif cleaned.kind_hint == "code":
            kind = "code"
        elif len(cleaned.lines) == 1 and _is_heading_line(text, indent):
            kind = "heading"
            section = new_section(text, _section_number(text))
        else:
            lm = _LIST_RE.match(first)
            numbered = _NUMBERED_SECTION_RE.match(first)
            if numbered and indent <= 3 and fmt != "md":
                # A top-level numbered clause ("0. This License applies ...")
                # opens a section even without a separate heading line.
                words = text.split()
                title = " ".join(words[:8]) + (" ..." if len(words) > 8 else "")
                section = new_section(title, numbered.group(1))
                label = numbered.group(1)
                kind = "list_item"
            elif lm:
                kind = "list_item"
                label = lm.group(2)
        pid = f"p{len(paragraphs) + 1:04d}"
        para = Paragraph(
            id=pid,
            index=len(paragraphs),
            text=text,
            kind=kind,
            section=section.key,
            label=label,
            indent=indent,
            line=cleaned.line,
            fingerprint=fingerprint(text),
        )
        paragraphs.append(para)
        section.para_ids.append(pid)

    if not sections[0].para_ids:
        sections = sections[1:]
    return Document(key=key, source=source, sha256=sha256, format=fmt, paragraphs=paragraphs, sections=sections)


def ingest_text(text: str, key: str = "A", source: str = "<text>", fmt: str = "txt") -> Document:
    """Ingest a string. ``fmt`` is 'txt' or 'md'."""
    data = text.encode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    blocks = _blocks_markdown(lines) if fmt == "md" else _split_blank(lines)
    return build_document(key, source, hashlib.sha256(data).hexdigest(), fmt, blocks)


def ingest_file(path: str | os.PathLike, key: str = "A") -> Document:
    p = Path(path)
    raw = p.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    suffix = p.suffix.lower()
    source = display_source(p)
    if suffix == ".pdf":
        return build_document(key, source, sha, "pdf", _blocks_pdf(p))
    text = raw.decode("utf-8", errors="replace")
    fmt = "md" if suffix in (".md", ".markdown") else "txt"
    doc = ingest_text(text, key=key, source=source, fmt=fmt)
    doc.sha256 = sha
    return doc
