import json

from conftest import CC, PLANTED, ROOT, TRUTH
from docaudit.align import align
from docaudit.evaluation import resolve_anchor
from docaudit.ingest import ingest_file, ingest_text

PARAS = [
    "Alpha clause: the supplier delivers the goods within ten days of the order.",
    "Bravo clause: the buyer pays the invoice within thirty days of delivery.",
    "Charlie clause: either party may terminate with sixty days written notice.",
    "Delta clause: notices are sent by registered mail to the addresses above.",
    "Echo clause: this agreement is governed by the law of the seller's seat.",
]


def doc(paras, key):
    return ingest_text("\n\n".join(paras) + "\n", key)


def ops_of(al):
    return [(o.op, o.a, o.b) for o in al.ops]


def test_identical_documents_align_equal():
    al = align(doc(PARAS, "A"), doc(PARAS, "B"))
    assert al.stats()["equal"] == 5 and len(al.changed_ops()) == 0


def test_modified_inserted_deleted():
    b = list(PARAS)
    b[1] = b[1].replace("thirty days", "sixty days")
    del b[3]
    b.insert(2, "Foxtrot clause: the supplier keeps spare parts available for five years.")
    al = align(doc(PARAS, "A"), doc(b, "B"))
    got = {(o.op, o.a, o.b) for o in al.ops}
    assert ("modified", "p0002", "p0002") in got
    assert ("inserted", None, "p0003") in got
    assert ("deleted", "p0004", None) in got
    mod = next(o for o in al.ops if o.op == "modified")
    assert 0.3 < mod.sim < 1.0


def test_move_is_detected():
    b = [PARAS[4]] + PARAS[:4]
    al = align(doc(PARAS, "A"), doc(b, "B"))
    assert ("moved", "p0005", "p0001") in ops_of(al)
    assert al.stats()["equal"] == 4


def test_ops_are_ordered_by_position_in_b():
    b = list(PARAS)
    del b[1]
    al = align(doc(PARAS, "A"), doc(b, "B"))
    assert [o.op for o in al.ops] == ["equal", "deleted", "equal", "equal", "equal"]


def test_planted_alignment_has_only_planted_differences():
    """Every changed operation between CC BY 4.0 and the planted copy maps to a ground-truth item,
    and the whitespace, typography and hyphenation edits produce no operation at all."""
    a, b = ingest_file(CC, "A"), ingest_file(PLANTED, "B")
    al = align(a, b)
    assert al.stats() == {"equal": 65, "modified": 12, "inserted": 2, "deleted": 1, "moved": 1}
    truth = json.loads((ROOT / TRUTH).read_text(encoding="utf-8"))
    item_paras = {}
    for it in truth["items"]:
        paras = {("A", resolve_anchor(a, x)) for x in it.get("anchors_a", [])}
        paras |= {("B", resolve_anchor(b, x)) for x in it.get("anchors_b", [])}
        item_paras[it["id"]] = paras
    for op in al.changed_ops():
        cited = {("A", op.a), ("B", op.b)}
        assert any(cited & p for p in item_paras.values()), f"unplanned difference at op {op.index}"
    by_id = {o.b: o for o in al.ops if o.b}
    for item in ("E02", "E03", "E05"):
        (pb,) = [pid for doc_key, pid in item_paras[item] if doc_key == "B"]
        assert by_id[pb].op == "equal", item


def test_section_pairs_cover_every_section():
    a, b = ingest_file(CC, "A"), ingest_file(PLANTED, "B")
    al = align(a, b)
    assert len(al.section_pairs) == len(a.sections)
    assert all(p["b"] is not None for p in al.section_pairs)
