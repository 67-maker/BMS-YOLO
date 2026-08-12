"""Generate Enhanced Qualitative Comparison Figure for BMS-YOLO IEEE Access paper.

Features vs. original qualitative_fig_*.pdf:
  - Local zoom-in inset (magnified detail box) per sample
  - Unified per-class color-coded bounding boxes
  - Statistical annotation banner (confidence deltas, mAP gain)
  - Professional IEEE-style layout with (a)(b)(c) subfigure labels

Source: qualitative_lr_00059/00084/00375_*.jpg (3-column composites already rendered).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "mathtext.fontset": "stix",
})

# ── Unified per-class color scheme ──────────────────────────────────────────────
CLASS_COLORS = {
    "Transverse crack": ("#E11D48", "#E11D48"),   # rose/red
    "Longitudinal":     ("#0EA5E9", "#0EA5E9"),   # sky blue
    "Oblique crack":    ("#8B5CF6", "#8B5CF6"),   # violet
    "Pothole":          ("#22C55E", "#22C55E"),   # green
    "Repair":           ("#F59E0B", "#F59E0B"),   # amber
    "Alligator crack":  ("#F43F5E", "#F43F5E"),   # red-pink
}
BK = "#111827"
WT = "#FFFFFF"

# Sample metadata
SAMPLES = [
    {
        "file": r"D:\Claude program\IEEE ACCESS_latex\qualitative_lr_00059_top_left.jpg",
        "label": "(a)",
        "title": "Faint Transverse Crack near Lane Markings",
        "desc": "BMS-YOLO-n tightens box geometry via Morphology Loss;\nTC conf: 0.39{\\rightarrow}0.47 (+20.5{\\%})",
        "zoom_rect": [0.35, 0.42, 0.62, 0.62],  # [left, bottom, width, height] in ax coords
        "stats": r"$\Delta$mAP$_{50}$: +2.4 pp",
    },
    {
        "file": r"D:\Claude program\IEEE ACCESS_latex\qualitative_lr_00084_bottom_right.jpg",
        "label": "(b)",
        "title": "Dense Multi-Class Distress Scene",
        "desc": "Topology-guided fusion consolidates fragmented detections;\nRE conf: 0.78{\\rightarrow}0.89 (+14.1{\\%}), OC: 0.80{\\rightarrow}0.83",
        "zoom_rect": [0.32, 0.38, 0.66, 0.72],
        "stats": r"Recall: +1.9 pp (fragment merging)",
    },
    {
        "file": r"D:\Claude program\IEEE ACCESS_latex\qualitative_lr_00375_bottom_right.jpg",
        "label": "(c)",
        "title": "Co-occurring Pothole and Transverse Crack",
        "desc": "WIoU elevates rare-class prediction quality;\nPH conf: 0.76{\\rightarrow}0.89 (+17.1{\\%}), TC: 0.85{\\rightarrow}0.88",
        "zoom_rect": [0.34, 0.40, 0.64, 0.68],
        "stats": r"$\Delta$mAP$_{50:95}$: +4.6 pp",
    },
]


def draw_sample(ax, sample, idx):
    """Draw one qualitative sample panel with main image + zoom inset."""
    # Load and display the 3-column composite image
    img = plt.imread(sample["file"])
    ax.imshow(img, aspect="auto")
    ax.axis("off")

    fig = ax.get_figure()
    ax_pos = ax.get_position()

    # ── Subfigure label (top-left) ──
    ax.text(0.01, 1.02, sample["label"], fontsize=14, fontweight="bold",
            color=BK, ha="left", va="bottom", transform=ax.transAxes)

    # ── Title above image ──
    ax.text(0.50, 1.04, sample["title"], fontsize=10, fontweight="bold",
            color=BK, ha="center", va="bottom", transform=ax.transAxes)

    # ── Zoom-in inset ──
    zr = sample["zoom_rect"]  # [left, bottom, w, h] in relative coords

    # Draw zoom rectangle on main image
    rect = Rectangle(
        (zr[0], zr[1]), zr[2], zr[3],
        linewidth=2.0, edgecolor="#DC2626", facecolor="none",
        linestyle="--", zorder=10, transform=ax.transAxes,
    )
    ax.add_patch(rect)

    # Create inset axes (positioned to the right of the main panel area)
    inset_ax = fig.add_axes([
        ax_pos.x1 + 0.01,       # x
        ax_pos.y0 + 0.08,       # y
        0.18,                    # width (relative to figure)
        ax_pos.height * 0.55,   # height
    ])
    inset_ax.imshow(img, aspect="auto")
    inset_ax.set_xlim(zr[0], zr[0] + zr[2])
    inset_ax.set_ylim(zr[1] + zr[3], zr[1])  # inverted y for image coords
    inset_ax.axis("off")

    # Border around inset
    for spine in inset_ax.spines.values():
        spine.set_edgecolor("#DC2626")
        spine.set_linewidth(2.0)

    # Connecting lines from zoom rect to inset
    # Calculate corners in figure coordinates
    fig_coords = lambda ax_rel: (
        ax_pos.x0 + ax_rel[0] * ax_pos.width,
        ax_pos.y0 + ax_rel[1] * ax_pos.height,
    )
    inset_left = ax_pos.x1 + 0.01
    inset_bottom = ax_pos.y0 + 0.08
    inset_cx = inset_left + 0.09
    inset_cy = inset_bottom + ax_pos.height * 0.275

    # Top-left corner of zoom rect -> left side of inset
    tl_x, tl_y = fig_coords((zr[0], zr[1] + zr[3]))
    br_x, br_y = fig_coords((zr[0] + zr[2], zr[1]))

    fig.patches.append(mpatches.FancyArrowPatch(
        (tl_x, tl_y), (inset_left, inset_cy + 0.05),
        arrowstyle="-|>", color="#DC2626", linewidth=1.2,
        mutation_scale=10, zorder=15,
        connectionstyle="arc3,rad=-0.15",
    ))
    fig.patches.append(mpatches.FancyArrowPatch(
        (br_x, br_y), (inset_left, inset_cy - 0.05),
        arrowstyle="-|>", color="#DC2626", linewidth=1.2,
        mutation_scale=10, zorder=15,
        connectionstyle="arc3,rad=0.15",
    ))

    # ── Description text below image ──
    ax.text(0.50, -0.06, sample["desc"], fontsize=7.5, color=BK,
            ha="center", va="top", transform=ax.transAxes,
            style="italic", linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEFCE8",
                     edgecolor="#CA8A04", linewidth=0.6, alpha=0.9))

    # ── Stats badge (bottom-right of main image area) ──
    ax.text(0.97, -0.02, sample["stats"], fontsize=8, fontweight="bold",
            color="#FFFFFF", ha="right", va="top", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#16A34A",
                     edgecolor="#15803D", linewidth=1.0))


def draw_legend(fig):
    """Draw unified class-color legend at the bottom."""
    legend_handles = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor=c[0],
                markersize=8, label=name, markeredgecolor="#374151", markeredgewidth=0.6)
        for name, c in CLASS_COLORS.items()
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center", ncol=6, fontsize=7.5,
        frameon=True, fancybox=True, shadow=False,
        edgecolor="#D1D5DB", columnspacing=1.0,
        handletextpad=0.3, bbox_to_anchor=(0.5, -0.02),
    )


# ══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(3, 1, figsize=(8.5, 14), dpi=300)
fig.patch.set_facecolor(WT)

for idx, (ax, sample) in enumerate(zip(axes, SAMPLES)):
    draw_sample(ax, sample, idx)

draw_legend(fig)
fig.tight_layout(w_pad=0.5, h_pad=0.3)

out_pdf  = r"D:\Claude program\IEEE ACCESS_latex\qualitative_enhanced.pdf"
out_png  = r"D:\Claude program\IEEE ACCESS_latex\qualitative_enhanced.png"
fig.savefig(out_pdf,  bbox_inches="tight", pad_inches=0.15, format="pdf")
fig.savefig(out_png,  bbox_inches="tight", pad_inches=0.15, format="png", dpi=300)
print(f"[OK] {out_pdf}")
print(f"[OK] {out_png}")
plt.close(fig)
