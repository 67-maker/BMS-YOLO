import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# IEEE Access two-column figure width ~7in; use larger canvas for high-res
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis('off')

# Color palette (light theme, print-friendly)
C_FDDE    = '#DBEAFE';  EC_FDDE    = '#2563EB'  # blue
C_MORPH   = '#FFEDD5';  EC_MORPH   = '#EA580C'  # orange
C_SPPF    = '#F3E8FF';  EC_SPPF    = '#9333EA'  # purple
C_HEAD    = '#DCFCE7';  EC_HEAD    = '#16A34A'  # green
C_POST    = '#CCFBF1';  EC_POST    = '#0D9488'  # teal
C_INPUT   = '#F3F4F6';  EC_INPUT   = '#4B5563'  # gray
C_WHITE   = '#FFFFFF';  EC_BLACK   = '#111827'

def box(ax, x, y, w, h, text, facecolor, edgecolor, fontsize=9, bold=True,
        radius=0.08, textcolor='black', ha='center', va='center'):
    """Draw a rounded rectangle with text."""
    fb = FancyBboxPatch((x, y), w, h,
                        boxstyle=f"round,pad=0.02,rounding_size={radius}",
                        facecolor=facecolor, edgecolor=edgecolor,
                        linewidth=1.5, zorder=2)
    ax.add_patch(fb)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, fontsize=fontsize, color=textcolor,
            ha=ha, va=va, weight=weight, wrap=True, zorder=3)
    return fb

def arrow(ax, x1, y1, x2, y2, color='#374151', style='->', lw=1.2,
          connectionstyle="arc3,rad=0", zorder=1):
    """Draw an arrow between two points."""
    if abs(x1 - x2) < 0.01 and abs(y1 - y2) < 0.01:
        return
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle=style, color=color,
                        linewidth=lw, connectionstyle=connectionstyle,
                        mutation_scale=12, zorder=zorder)
    ax.add_patch(a)
    return a

def arrow_between_boxes(ax, b1, b2, color='#374151', style='->', lw=1.2,
                        connectionstyle="arc3,rad=0", offset1=(0,0), offset2=(0,0)):
    """Draw arrow from center/right of b1 to center/left of b2."""
    x1, y1, w1, h1 = b1.get_bbox().bounds
    x2, y2, w2, h2 = b2.get_bbox().bounds
    # default: right center of b1 to left center of b2
    sx = x1 + w1 + offset1[0]
    sy = y1 + h1/2 + offset1[1]
    ex = x2 + offset2[0]
    ey = y2 + h2/2 + offset2[1]
    arrow(ax, sx, sy, ex, ey, color=color, style=style, lw=lw,
          connectionstyle=connectionstyle)

# Title
ax.text(7, 7.6, 'Overall architecture of BMS-YOLO', fontsize=18, ha='center',
        va='center', weight='bold', color=EC_BLACK)
ax.text(7, 7.25, 'Input 640×640 → Stem+FDDE → Backbone (BMSC2f+MorphSparseMoE) → Neck → Head → Post-processing',
        fontsize=10, ha='center', va='center', color='#4B5563')

# ---------- Left column: Input + Stem + FDDE ----------
inp = box(ax, 0.4, 3.5, 1.4, 1.2, 'Input Image\n640×640×3',
          C_INPUT, EC_INPUT, fontsize=10)

stem = box(ax, 2.3, 3.2, 2.4, 1.8,
           'Stem + FDDE\nConv 6×6, s=2\n320×320×64',
           C_FDDE, EC_FDDE, fontsize=10)

# ---------- Backbone column ----------
ax.text(6.0, 6.85, 'Backbone', fontsize=12, ha='center', weight='bold', color=EC_BLACK)

p2 = box(ax, 5.0, 5.8, 2.0, 1.0,
         'BMSC2f ×1\nMorphSparseMoE\n320×320×64',
         C_MORPH, EC_MORPH, fontsize=9)

p3 = box(ax, 5.0, 4.5, 2.0, 1.0,
         'BMSC2f ×2\nMorphSparseMoE\n160×160×128',
         C_MORPH, EC_MORPH, fontsize=9)

p4 = box(ax, 5.0, 3.2, 2.0, 1.0,
         'BMSC2f ×2\nMorphSparseMoE\n80×80×256',
         C_MORPH, EC_MORPH, fontsize=9)

p5 = box(ax, 5.0, 1.9, 2.0, 1.0,
         'BMSC2f ×1\nMorphSparseMoE\n40×40×512',
         C_MORPH, EC_MORPH, fontsize=9)

# Downsample arrows inside backbone
arrow(ax, 6.0, 5.8, 6.0, 5.5, color='#374151')
arrow(ax, 6.0, 4.5, 6.0, 4.2, color='#374151')
arrow(ax, 6.0, 3.2, 6.0, 2.9, color='#374151')

# ---------- Neck ----------
ax.text(9.1, 6.85, 'Neck', fontsize=12, ha='center', weight='bold', color=EC_BLACK)

sppf = box(ax, 8.0, 1.9, 2.2, 1.0,
           'LightSPPFCSPC\n+ ECA Attention\n40×40×512',
           C_SPPF, EC_SPPF, fontsize=9)

neck = box(ax, 8.0, 3.8, 2.2, 1.8,
           'Multi-Scale Fusion\nFPN (Top-Down)\n+ PAN (Bottom-Up)\nP3 / P4 / P5',
           C_SPPF, EC_SPPF, fontsize=9)

# ---------- Detection Head ----------
ax.text(12.3, 6.85, 'Decoupled Detection Head', fontsize=12, ha='center', weight='bold', color=EC_BLACK)

h3 = box(ax, 11.2, 5.5, 2.2, 0.9,
         'P3 Head\n160×160\nCls  +  BBox',
         C_HEAD, EC_HEAD, fontsize=9)

h4 = box(ax, 11.2, 4.2, 2.2, 0.9,
         'P4 Head\n80×80\nCls  +  BBox',
         C_HEAD, EC_HEAD, fontsize=9)

h5 = box(ax, 11.2, 2.9, 2.2, 0.9,
         'P5 Head\n40×40\nCls  +  BBox',
         C_HEAD, EC_HEAD, fontsize=9)

# ---------- Post-processing ----------
post = box(ax, 7.5, 0.35, 5.0, 1.15,
           'Post-Processing\nNMS → Topology Fusion\n(Union-Find)',
           C_POST, EC_POST, fontsize=9)

final = box(ax, 13.2, 0.575, 1.3, 0.7,
            'Final\nDetections',
            C_INPUT, EC_INPUT, fontsize=10)

# ---------- Arrows ----------
# Input -> Stem
arrow_between_boxes(ax, inp, stem)
# Stem -> P2
arrow_between_boxes(ax, stem, p2)
# P5 -> SPPFCSPC
arrow_between_boxes(ax, p5, sppf)
# SPPFCSPC -> Neck fusion
arrow(ax, 9.1, 2.9, 9.1, 3.8, color='#374151')
# P3 -> Neck (FPN top-down skip)
arrow(ax, 7.0, 5.0, 8.0, 5.0, color='#6B7280', style='->', connectionstyle="arc3,rad=0.1")
# P4 -> Neck
arrow(ax, 7.0, 3.7, 8.0, 4.4, color='#6B7280', style='->', connectionstyle="arc3,rad=0.1")
# Neck -> P3 Head
arrow(ax, 10.2, 5.0, 11.2, 5.95, color='#374151')
# Neck -> P4 Head
arrow(ax, 10.2, 4.7, 11.2, 4.65, color='#374151')
# Neck -> P5 Head
arrow(ax, 10.2, 4.4, 11.2, 3.35, color='#374151')
# Heads -> Post-processing
arrow(ax, 12.3, 5.5, 12.3, 1.5, color='#374151', connectionstyle="arc3,rad=-0.2")
arrow(ax, 12.3, 4.65, 12.0, 1.5, color='#374151', connectionstyle="arc3,rad=-0.15")
arrow(ax, 12.3, 2.9, 11.7, 1.5, color='#374151', connectionstyle="arc3,rad=-0.1")
# Post -> Final
arrow_between_boxes(ax, post, final)

# ---------- Legend ----------
legend_items = [
    (C_FDDE, EC_FDDE, 'FDDE Module'),
    (C_MORPH, EC_MORPH, 'BMSC2f + MoE'),
    (C_SPPF, EC_SPPF, 'SPPFCSPC + ECA'),
    (C_HEAD, EC_HEAD, 'Detection Head'),
    (C_POST, EC_POST, 'Post-Processing'),
]
leg_x, leg_y = 1.4, 0.15
for i, (fc, ec, label) in enumerate(legend_items):
    lx = leg_x + i * 2.65
    rect = FancyBboxPatch((lx, leg_y), 0.35, 0.25,
                          boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=2)
    ax.add_patch(rect)
    ax.text(lx + 0.45, leg_y + 0.12, label, fontsize=8, va='center',
            color=EC_BLACK, clip_on=False)

# Save outputs
out_pdf = r'D:\Claude program\IEEE ACCESS_latex\figure1_architecture.pdf'
out_png = r'D:\Claude program\IEEE ACCESS_latex\figure1_architecture.png'
plt.savefig(out_pdf, bbox_inches='tight', pad_inches=0.05, format='pdf')
plt.savefig(out_png, bbox_inches='tight', pad_inches=0.05, format='png', dpi=300)
print(f'Saved: {out_pdf}')
print(f'Saved: {out_png}')
