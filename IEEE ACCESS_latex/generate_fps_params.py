"""Regenerate Fig.2 (FPS vs. Parameters scatter) for BMS-YOLO IEEE Access paper.

Data source: Table 2 in access_final.tex. FPS values are the user's measured
benchmarks (imgsz=640, warmup 50, formal 200). Point size encodes mAP50.
Color palette is reused from figure1_architecture.pdf for visual consistency.
All models share the same marker/edge treatment ("all equal style").
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# IEEE Access: use a serif (Times-like) font to match the document body
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "mathtext.fontset": "stix",
    "axes.linewidth": 1.0,
})

# --- Palette reused from figure1_architecture.pdf (Fig.1 hue family) ---
C_BLUE   = "#2563EB"
C_ORANGE = "#EA580C"
C_PURPLE = "#9333EA"
C_GREEN  = "#16A34A"
C_TEAL   = "#0D9488"
C_GRAY   = "#4B5563"
EC_BLACK = "#111827"

# Model data: (label, Params[M], FPS, mAP50[%], color)
models = [
    ("YOLOv8n",   3.01, 46.4, 76.9, C_BLUE),
    ("YOLOv9t",   7.0,  38.9, 71.9, C_ORANGE),
    ("YOLOv10n",  2.7,  45.2, 79.5, C_PURPLE),
    ("YOLOv11n",  2.6,  44.3, 77.8, C_GREEN),
    ("RT-DETR-l", 32.8, 26.9, 72.9, C_TEAL),
    ("BMS-YOLO-n", 3.8, 32.3, 79.3, C_GRAY),
]

# Manual label offsets (in points) to avoid overlap of the lightweight cluster
label_offsets = {
    "YOLOv8n":   (6, 9),
    "YOLOv10n":  (9, -18),
    "YOLOv11n":  (-38, -18),
    "YOLOv9t":   (6, 7),
    "RT-DETR-l": (8, 6),
    "BMS-YOLO-n": (7, 5),
}

fig, ax = plt.subplots(figsize=(8.2, 5.4), dpi=300)

# Map mAP50 (71.9 .. 79.5) -> scatter size (points^2)
def size_of(m):
    return 90.0 + (m - 70.0) * 34.0

for name, p, fps, m, color in models:
    ax.scatter(
        p, fps,
        s=size_of(m),
        c=color,
        edgecolors=EC_BLACK,
        linewidths=1.1,
        alpha=0.9,
        zorder=3,
    )
    dx, dy = label_offsets[name]
    ax.annotate(
        name,
        (p, fps),
        textcoords="offset points",
        xytext=(dx, dy),
        fontsize=9,
        color=EC_BLACK,
        zorder=4,
    )

ax.set_xscale("log")
ax.set_xlabel("Parameters (M)", fontsize=11)
ax.set_ylabel("FPS (batch-size 1)", fontsize=11)
ax.tick_params(axis="both", which="major", labelsize=9.5)
ax.grid(True, which="both", linestyle=":", alpha=0.45, zorder=0)

# Axis limits with a little breathing room
ax.set_xlim(2.2, 40)
ax.set_ylim(20, 52)

# Note explaining the encoded variable
ax.text(
    0.98, 0.04,
    "Point size encodes mAP50",
    transform=ax.transAxes,
    fontsize=8.5,
    color="#6B7280",
    ha="right",
    va="bottom",
)

fig.tight_layout()
fig.savefig("fig6_fps_params.pdf", bbox_inches="tight", pad_inches=0.05)
fig.savefig("fig6_fps_params.png", bbox_inches="tight", pad_inches=0.05, dpi=200)
print("Fig.2 regenerated: fig6_fps_params.pdf / .png")
