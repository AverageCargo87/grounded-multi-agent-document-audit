from pathlib import Path

import pytest

from conftest import CC, GPL2, GPL3
from docaudit.ingest import display_source, ingest_file, ingest_text

TEXT = """Title Of The Thing

Section 1 -- Definitions.

  a. Widget means a small device that is
     used by the Operator.

  b. Operator means the person who runs
     the widget.

Section 2 -- Duties.

The Operator must inspect the widget within 30 days of delivery and
must keep a written record of every inspection.
"""


def test_ids_are_sequential_and_stable():
    d1 = ingest_text(TEXT)
    d2 = ingest_text(TEXT)
    assert [p.id for p in d1.paragraphs] == [f"p{i:04d}" for i in range(1, len(d1.paragraphs) + 1)]
    assert [(p.id, p.fingerprint, p.text) for p in d1.paragraphs] == [(p.id, p.fingerprint, p.text) for p in d2.paragraphs]


def test_ids_and_fingerprints_survive_rewrap_and_crlf():
    rewrapped = TEXT.replace("that is\n     used", "that is used").replace("\n", "\r\n")
    a, b = ingest_text(TEXT), ingest_text(rewrapped)
    assert [p.id for p in a.paragraphs] == [p.id for p in b.paragraphs]
    assert [p.fingerprint for p in a.paragraphs] == [p.fingerprint for p in b.paragraphs]


def test_sections_headings_and_list_items():
    d = ingest_text(TEXT)
    titles = [s.title for s in d.sections]
    assert "Section 1 -- Definitions." in titles and "Section 2 -- Duties." in titles
    sec1 = next(s for s in d.sections if s.number == "1")
    kinds = [d.para(pid).kind for pid in sec1.para_ids]
    assert kinds == ["heading", "list_item", "list_item"]
    assert [d.para(pid).label for pid in sec1.para_ids[1:]] == ["a", "b"]
    assert d.para(sec1.para_ids[1]).text == "a. Widget means a small device that is used by the Operator."


def test_decoration_lines_are_dropped():
    d = ingest_text("Heading\n\n=========\n\nBody text here.\n")
    assert [p.text for p in d.paragraphs] == ["Heading", "Body text here."]


def test_markdown_headings_bullets_and_code():
    md = "# Title\n\nIntro line one\nline two.\n\n- first item\n- second item\n\n```\ncode block\n\nstill code\n```\n\n## Next\n\nMore text.\n"
    d = ingest_text(md, fmt="md")
    kinds = [(p.kind, p.text.splitlines()[0]) for p in d.paragraphs]
    assert kinds[0] == ("heading", "# Title")
    assert ("para", "Intro line one line two.") in kinds
    assert [p.text for p in d.paragraphs if p.text.startswith("-")] == ["- first item", "- second item"]
    code = next(p for p in d.paragraphs if p.kind == "code")
    assert "still code" in code.text
    assert [s.title for s in d.sections] == ["Title", "Next"]


def test_line_break_hyphen_is_kept_for_normalisation():
    d = ingest_text("The rights are non-\nexclusive and essen-\ntially free.\n")
    assert d.paragraphs[0].text == "The rights are non-exclusive and essen-tially free."


def test_demo_documents_regression():
    gpl2, gpl3, cc = ingest_file(GPL2), ingest_file(GPL3), ingest_file(CC)
    assert (len(gpl2.paragraphs), len(gpl3.paragraphs), len(cc.paragraphs)) == (59, 122, 79)
    assert [s.number for s in gpl3.sections if s.number] == [str(i) for i in range(18)]
    assert [s.number for s in cc.sections if s.number] == [str(i) for i in range(1, 9)]
    assert gpl2.sha256 == "8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643"


def test_display_source_never_absolute(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text("x\n", encoding="utf-8")
    assert display_source(p) == "doc.txt"
    assert display_source("examples/gpl/GPL-2.0.txt") == "examples/gpl/GPL-2.0.txt"
    assert not Path(ingest_file(p).source).is_absolute()


def test_pdf_ingest(tmp_path):
    fitz = pytest.importorskip("fitz")
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "Section 1 -- Scope.", fontsize=11)
    page.insert_text((72, 120), "The licensee must report within 30 days.", fontsize=11)
    path = tmp_path / "t.pdf"
    pdf.save(path)
    pdf.close()
    d = ingest_file(path)
    texts = [p.text for p in d.paragraphs]
    assert "Section 1 -- Scope." in texts
    assert "The licensee must report within 30 days." in texts
    assert d.format == "pdf" and d.paragraphs[0].line == 1
