"""Markdown renderings that agents read. Every paragraph is tagged [doc:pNNNN]."""

from __future__ import annotations

from .align import EQUAL, Alignment, Op
from .ingest import Document, Paragraph


def tag(doc_key: str, p: Paragraph) -> str:
    return f"[{doc_key}:{p.id}]"


def para_line(doc_key: str, p: Paragraph) -> str:
    return f"{tag(doc_key, p)} {p.text}"


def render_document(doc: Document) -> str:
    out = [f"# Document {doc.key}: {doc.source}", "", f"{len(doc.paragraphs)} paragraphs. Quote from the text after each tag.", ""]
    for p in doc.paragraphs:
        if p.kind == "heading":
            out.append("")
            out.append(f"## {tag(doc.key, p)} {p.text}")
            out.append("")
        else:
            out.append(para_line(doc.key, p))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def _section_title(doc: Document, pid: str) -> str:
    sec = doc.section_of(pid)
    return sec.title if sec else ""


def render_op(op: Op, docs: dict[str, Document], full_equal: bool = False) -> list[str]:
    a, b = docs["A"], docs["B"]
    pa = a.para(op.a) if op.a else None
    pb = b.para(op.b) if op.b else None
    where = _section_title(b, op.b) if op.b else _section_title(a, op.a)
    lines: list[str] = []
    if op.op == EQUAL and not full_equal:
        snippet = pb.text if len(pb.text) <= 90 else pb.text[:87] + "..."
        lines.append(f"### Op {op.index}: EQUAL  [A:{op.a}] = [B:{op.b}]  {snippet}")
        return lines
    label = {"modified": f"MODIFIED (similarity {op.sim:.2f})", "inserted": "INSERTED in B", "deleted": "DELETED from A",
             "moved": f"MOVED (similarity {op.sim:.2f})", "equal": "EQUAL"}[op.op]
    lines.append(f"### Op {op.index}: {label}  (section: {where})")
    lines.append("")
    if pa:
        lines.append(para_line("A", pa))
        lines.append("")
    if pb:
        lines.append(para_line("B", pb))
        lines.append("")
    return lines


def render_diff_chunk(chunk: dict, alignment: Alignment, docs: dict[str, Document]) -> str:
    out = [
        f"# Chunk {chunk['id']} (diff mode: A = {docs['A'].source}, B = {docs['B'].source})",
        "",
        "Each entry below is one alignment operation computed by code. EQUAL entries are listed for context only.",
        f"Sections: {'; '.join(chunk['titles'])}",
        "",
    ]
    for idx in chunk["ops"]:
        out.extend(render_op(alignment.ops[idx], docs))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_audit_chunk(chunk: dict, doc: Document) -> str:
    out = [f"# Chunk {chunk['id']} (audit mode: {doc.source})", "", f"Sections: {'; '.join(chunk['titles'])}", ""]
    current = None
    for pid in chunk["paras"]["A"]:
        p = doc.para(pid)
        if p.section != current:
            current = p.section
            sec = doc.section_of(pid)
            out.append(f"## Section: {sec.title}")
            out.append("")
        out.append(para_line("A", p))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_index(mode: str, docs: dict[str, Document], alignment: Alignment | None, refs: dict, terms: dict,
                 numbers: dict, sweeps: list[dict]) -> str:
    out = [f"# Deterministic index ({mode} mode)", ""]
    for key, doc in docs.items():
        out.append(f"## Outline of document {key}: {doc.source}")
        out.append("")
        for s in doc.sections:
            rng = f"{s.para_ids[0]}..{s.para_ids[-1]}" if s.para_ids else "-"
            out.append(f"- {s.title} ({rng})")
        out.append("")
        out.append(f"## Defined terms in {key}")
        out.append("")
        if terms[key]:
            for t, pid in terms[key].items():
                out.append(f"- \"{t}\" defined at [{key}:{pid}]")
        else:
            out.append("- none detected")
        out.append("")
        out.append(f"## Cross-references in {key} (resolved by code)")
        out.append("")
        for r in refs[key]:
            status = r["status"] + (f" ({r['detail']})" if r["detail"] else "")
            out.append(f"- [{key}:{r['para_id']}] \"{r['text']}\": {status}")
        if not refs[key]:
            out.append("- none detected")
        out.append("")
        out.append(f"## Numeric expressions in {key}")
        out.append("")
        for n in numbers[key]:
            out.append(f"- [{key}:{n['para_id']}] {n['value']}: ...{n['context']}...")
        if not numbers[key]:
            out.append("- none detected")
        out.append("")
    if alignment is not None:
        st = alignment.stats()
        out.append("## Alignment summary (A -> B)")
        out.append("")
        out.append(", ".join(f"{k}: {v}" for k, v in st.items()))
        out.append("")
        for op in alignment.ops:
            if op.op in ("inserted", "deleted", "moved"):
                side, pid = ("B", op.b) if op.b else ("A", op.a)
                text = docs[side].para(pid).text
                words = " ".join(text.split()[:14])
                extra = f" (from [A:{op.a}])" if op.op == "moved" else ""
                out.append(f"- Op {op.index} {op.op.upper()} [{side}:{pid}]{extra}: {words} ...")
        out.append("")
    out.append("## Deterministic sweep findings (already in the pipeline; do not repeat them)")
    out.append("")
    for f in sweeps:
        ev = ", ".join(f"[{e['doc']}:{e['para_id']}]" for e in f["evidence"])
        out.append(f"- {f['kind']}: {f['title']} {ev}")
    if not sweeps:
        out.append("- none")
    return "\n".join(out).rstrip() + "\n"


def render_ops_list(title: str, intro: str, ops: list[Op], docs: dict[str, Document]) -> str:
    out = [f"# {title}", "", intro, ""]
    for op in ops:
        out.extend(render_op(op, docs, full_equal=True))
        out.append("")
    if not ops:
        out.append("No operations listed. Write an output with an empty findings list.")
    return "\n".join(out).rstrip() + "\n"


def render_findings_batch(title: str, findings: list[dict], docs: dict[str, Document], alignment: Alignment | None) -> str:
    out = [f"# {title}", ""]
    if not findings:
        out.append("This batch is empty. Write an output with empty verdicts and missed lists.")
        return "\n".join(out) + "\n"
    out.append("Each finding passed quote verification. Try to refute it. Paragraph texts are given in full.")
    out.append("")
    a2op = alignment.op_of_para() if alignment else {}
    for f in findings:
        out.append(f"## {f['id']} [{f['severity']}] {f['kind']}: {f['title']}")
        out.append("")
        out.append(f"Confidence {f['confidence']:.2f}. Reported by: {', '.join(f['sources'])}.")
        out.append("")
        out.append(f["description"])
        out.append("")
        out.append("Evidence:")
        shown = set()
        for e in f["evidence"]:
            out.append(f"- [{e['doc']}:{e['para_id']}] \"{e['quote']}\"")
        out.append("")
        out.append("Cited paragraphs (and their aligned counterparts):")
        out.append("")
        for e in f["evidence"]:
            key = (e["doc"], e["para_id"])
            if key in shown:
                continue
            shown.add(key)
            p = docs[e["doc"]].para(e["para_id"])
            out.append(para_line(e["doc"], p))
            out.append("")
            if alignment is not None and key in a2op:
                op = alignment.ops[a2op[key]]
                other = ("B", op.b) if e["doc"] == "A" else ("A", op.a)
                if other[1] and other not in shown:
                    shown.add(other)
                    out.append(f"(aligned as op {op.index} {op.op.upper()}) " + para_line(other[0], docs[other[0]].para(other[1])))
                    out.append("")
                elif not other[1]:
                    out.append(f"(op {op.index}: {op.op.upper()}, no counterpart in {'B' if e['doc'] == 'A' else 'A'})")
                    out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_editor_input(agg: dict) -> str:
    out = ["# Editor input", "", "Findings below survived quote verification and the skeptic stage. Severity and confidence are final.", ""]
    for f in agg["findings"]:
        out.append(f"## {f['id']} [{f['severity']}] {f['kind']} (confidence {f['confidence']:.2f}, {f['status']})")
        out.append("")
        out.append(f"**{f['title']}**")
        out.append("")
        out.append(f["description"])
        out.append("")
        for e in f["evidence"]:
            out.append(f"- [{e['doc']}:{e['para_id']}] \"{e['quote']}\"")
        for v in f.get("verdicts", []):
            out.append(f"- skeptic ({v['effective']}): {v['reason']}")
        out.append("")
    if agg.get("low_confidence"):
        out.append("## Low-confidence findings (list them under a separate theme if you mention them)")
        out.append("")
        for f in agg["low_confidence"]:
            out.append(f"- {f['id']} [{f['severity']}] {f['title']} (confidence {f['confidence']:.2f})")
    return "\n".join(out).rstrip() + "\n"
