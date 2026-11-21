"""Render docs/hero.png: the deterministic paragraph alignment of GPL-2.0 vs GPL-3.0.

Every cell is the token similarity of one GPL-2.0 paragraph (row) and one
GPL-3.0 paragraph (column); the markers are the pairs the aligner kept. No
model is involved. Needs matplotlib (CPU only).

Usage: python scripts/render_hero.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from docaudit.align import _Sim, align  # noqa: E402
from docaudit.ingest import ingest_file  # noqa: E402

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e4e3df"
BLUE_RAMP = [SURFACE, "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
MODIFIED = "#eb6834"  # categorical slot 2
EQUAL = "#1baf7a"  # categorical slot 3
MOVED = "#6250d6"  # categorical slot 7


def main() -> None:
    a = ingest_file(ROOT / "examples/gpl/GPL-2.0.txt", "A")
    b = ingest_file(ROOT / "examples/gpl/GPL-3.0.txt", "B")
    al = align(a, b)
    sim = _Sim(a, b)
    grid = [[sim(i, j) for j in range(len(b.paragraphs))] for i in range(len(a.paragraphs))]
    st = al.stats()

    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    cmap = LinearSegmentedColormap.from_list("seq_blue", BLUE_RAMP)
    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=1, aspect="auto", interpolation="nearest", origin="upper")

    a_idx = {p.id: p.index for p in a.paragraphs}
    b_idx = {p.id: p.index for p in b.paragraphs}
    for kind, color, marker, size in (("modified", MODIFIED, "o", 34), ("equal", EQUAL, "s", 34), ("moved", MOVED, "D", 34)):
        xs = [b_idx[o.b] for o in al.ops if o.op == kind]
        ys = [a_idx[o.a] for o in al.ops if o.op == kind]
        if xs:
            ax.scatter(xs, ys, s=size, c=color, marker=marker, edgecolors=SURFACE, linewidths=1.5, zorder=3)
    ins = [b_idx[o.b] for o in al.ops if o.op == "inserted"]
    dele = [a_idx[o.a] for o in al.ops if o.op == "deleted"]
    ax.plot(ins, [-1.6] * len(ins), "|", color=TEXT_2, markersize=7, clip_on=False)
    ax.plot([len(b.paragraphs) + 0.6] * len(dele), dele, "_", color=TEXT_2, markersize=7, clip_on=False)

    ax.set_xlim(-0.5, len(b.paragraphs) - 0.5)
    ax.set_ylim(len(a.paragraphs) - 0.5, -0.5)
    ax.set_xlabel("GPL-3.0 paragraph (B)", color=TEXT_2, fontsize=10)
    ax.set_ylabel("GPL-2.0 paragraph (A)", color=TEXT_2, fontsize=10)
    ax.tick_params(colors=TEXT_2, labelsize=8, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle("Deterministic paragraph alignment before any agent runs", x=0.06, y=0.97, ha="left",
                 fontsize=15, color=TEXT, fontweight="bold")
    fig.text(0.06, 0.915,
             f"GPL-2.0 ({len(a.paragraphs)} paragraphs, rows) vs GPL-3.0 ({len(b.paragraphs)} paragraphs, columns). "
             "Cell shade = token similarity of the two paragraphs; markers = pairs the aligner kept.",
             ha="left", fontsize=9.5, color=TEXT_2)
    fig.text(0.06, 0.885,
             f"{st['equal']} equal, {st['modified']} modified, {st['moved']} moved; {st['inserted']} paragraphs only in B "
             f"(ticks above), {st['deleted']} only in A (ticks right). Each changed pair becomes reader input.",
             ha="left", fontsize=9.5, color=TEXT_2)

    handles = [
        Line2D([], [], marker="s", linestyle="", color=EQUAL, markersize=7, label=f"equal pair ({st['equal']})"),
        Line2D([], [], marker="o", linestyle="", color=MODIFIED, markersize=7, label=f"modified pair ({st['modified']})"),
        Line2D([], [], marker="|", linestyle="", color=TEXT_2, markersize=9, label=f"inserted / deleted ({st['inserted']} / {st['deleted']})"),
    ]
    leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.055, 0.86), ncol=3, frameon=False,
                     fontsize=9, labelcolor=TEXT, handletextpad=0.4, columnspacing=1.8)
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.03)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=TEXT_2, labelsize=8, length=0)
    cbar.set_label("similarity", color=TEXT_2, fontsize=9)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.78, bottom=0.09)
    out = ROOT / "docs" / "hero.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, facecolor=SURFACE)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
