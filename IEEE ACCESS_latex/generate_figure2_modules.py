"""Generate Figure 2 — Module Structure Sub-diagrams for BMS-YOLO IEEE Access paper.

Three subfigures: (a) FDDE, (b) MorphSparseMoE, (c) SPPF-CSPC+ECA.
Vector PDF @ 300 dpi, matches Fig.1 palette.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "mathtext.fontset": "stix",
})

# Palette (Fig.1 consistent)
BF, BE = "#DBEAFE", "#2563EB"       # blue   – high-freq / FDDE
OF, OE = "#FFEDD5", "#EA580C"       # orange – MoE experts
PF, PE = "#F3E8FF", "#9333EA"       # purple – SPPF / pooling
GF, GE = "#DCFCE7", "#16A34A"       # green  – output / fusion
TF, TE = "#CCFBF1", "#0D9488"       # teal   – gating / router / ECA
RF, RE = "#FEE2E2", "#DC2626"       # red    – emphasis
YF, YE = "#FEF9C3", "#CA8A04"       # yellow – low-freq
KF, KE = "#F3F4F6", "#4B5563"       # gray   – generic
BK  = "#111827"
DK  = "#374151"
WT  = "#FFFFFF"

def rb(ax, x, y, w, h, txt, fc, ec, fs=9, bold=True, r=0.08, tc=BK,
        lw=1.2, zo=2):
    p = FancyBboxPatch((x,y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zo)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, txt, fontsize=fs, color=tc,
            ha="center", va="center",
            weight=("bold" if bold else "normal"), zorder=zo+1)
    return p

def ar(ax, x1, y1, x2, y2, c=DK, lw=0.95, cs="arc3,rad=0", zo=1, ms=11):
    if abs(x1-x2)<1e-4 and abs(y1-y2)<1e-4:
        return
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),
        arrowstyle="-|>", color=c, linewidth=lw,
        connectionstyle=cs, mutation_scale=ms, zorder=zo))

def lbl(ax, ch, x, y):
    ax.text(x, y, f"({ch})", fontsize=13, fontweight="bold",
            color=BK, ha="center", va="center")


# ══════════════════════════════════════════════════════════════════════════════
#  (a) FDDE
# ══════════════════════════════════════════════════════════════════════════════

def draw_fdde(ax):
    ax.set_xlim(0, 17); ax.set_ylim(0, 12); ax.axis("off")
    ax.set_title("FDDE Module", fontsize=14, fontweight="bold", color=BK, pad=6)

    inp = rb(ax, 0.3, 8.5, 2.0, 1.3, r"$X{\in}\mathbb{R}^{C{\times}H{\times}W}$", KF, KE, fs=10)
    ap  = rb(ax, 3.0, 9.0, 1.8, 0.75, r"AvgPool $3{\times}3$", KF, KE, fs=9)
    sub = rb(ax, 3.0, 7.7, 1.8, 0.75, r"$X_{\rm hi}{=}X{-}X_{\rm lo}$", KF, KE, fs=8)

    ar(ax, 2.3, 9.15, 3.0, 9.35, lw=0.85)
    ar(ax, 3.9, 9.0, 3.9, 8.45, lw=0.85)
    ar(ax, 2.3, 9.15, 3.0, 8.05, lw=0.85)

    dw5 = rb(ax, 5.6, 9.8, 1.7, 0.7, r"DWConv $1{\times}5$", BF, BE, fs=9)
    dw1 = rb(ax, 5.6, 8.8, 1.7, 0.7, r"DWConv $5{\times}1$", BF, BE, fs=9)
    sm  = rb(ax, 5.8, 7.75, 1.3, 0.6, r"$\Sigma$", BF, BE, fs=11, bold=True)
    ph  = rb(ax, 5.6, 6.7, 2.0, 0.7, r"Conv $1{\times}1$\n$X'_{\rm hi}$", BF, BE, fs=9)
    pl  = rb(ax, 5.6, 5.5, 2.0, 0.7, r"Conv $1{\times}1$\n$X'_{\rm lo}$", YF, YE, fs=9)

    ar(ax, 3.9, 7.7, 5.6, 10.15, lw=0.85)
    ar(ax, 3.9, 7.7, 5.6, 9.15, lw=0.85)
    ar(ax, 6.45, 9.8, 6.45, 8.35, lw=0.85)
    ar(ax, 6.45, 8.8, 6.6, 8.35, lw=0.85)
    ar(ax, 6.45, 7.75, 6.45, 7.4, lw=0.85)
    ar(ax, 3.9, 7.7, 5.6, 5.85, lw=0.85)

    gt  = rb(ax, 8.2, 9.65, 1.35, 0.6, "GAP", TF, TE, fs=10, bold=True)
    sg  = rb(ax, 8.2, 8.75, 1.35, 0.6, r"$\sigma$", TF, TE, fs=12, bold=True)
    g   = rb(ax, 8.05, 7.7, 1.65, 0.7, r"$G{\in}(0{,}1)^C$", TF, TE, fs=9)

    ar(ax, 3.9, 7.7, 8.2, 9.95, lw=0.85)
    ar(ax, 8.87, 9.65, 8.87, 9.35, lw=0.85)
    ar(ax, 8.87, 8.75, 8.87, 8.4, lw=0.85)

    mh  = rb(ax, 8.2, 6.55, 1.65, 0.6, r"$G{\odot}X'_{\rm hi}$", BF, BE, fs=8)
    ml  = rb(ax, 8.2, 5.6, 1.65, 0.6, r"$(1{-}G){\odot}X'_{\rm lo}$", YF, YE, fs=7.5)
    ct  = rb(ax, 8.15, 4.55, 1.75, 0.6, r"Concat\n${[}{\cdot}{;}{\cdot}{]}$", KF, KE, fs=9)
    cf  = rb(ax, 8.0, 3.6, 2.0, 0.75, r"Conv $1{\times}1$", GF, GE, fs=10)

    ar(ax, 8.87, 7.7, 8.87, 7.15, lw=0.85)
    ar(ax, 8.87, 5.5, 8.87, 6.2, lw=0.85)
    ar(ax, 6.6, 7.05, 8.2, 6.85, lw=0.85)
    ar(ax, 6.6, 5.85, 8.2, 5.9, lw=0.85)
    ar(ax, 9.02, 6.55, 9.02, 5.15, lw=0.85)
    ar(ax, 9.02, 5.6, 9.02, 5.15, lw=0.85)
    ar(ax, 9.02, 4.55, 9.02, 4.35, lw=0.85)

    add = rb(ax, 10.6, 5.5, 0.7, 0.7, "$+$", GF, GE, fs=14, bold=True)
    out = rb(ax, 11.8, 5.25, 2.2, 1.2, r"$X_{\rm out}$\nOutput", GF, GE, fs=11, bold=True)

    ar(ax, 10.0, 3.97, 10.6, 5.85, lw=0.95)
    ar(ax, 2.3, 9.15, 10.6, 5.85, c=RE, lw=0.95, cs="arc3,rad=0.18")
    ar(ax, 11.3, 5.85, 11.8, 5.85, lw=0.95)

    ax.text(6.45, 10.7, "High-Frequency Branch", fontsize=9, color=BE, ha="center", fontstyle="italic")
    ax.text(6.6, 4.9, "Low-Frequency Branch", fontsize=9, color=YE, ha="center", fontstyle="italic")
    ax.text(9.02, 10.7, "Adaptive Gating", fontsize=9, color=TE, ha="center", fontstyle="italic")

    lbl(ax, "a", 0.5, 11.4)


# ══════════════════════════════════════════════════════════════════════════════
#  (b) MorphSparseMoE
# ══════════════════════════════════════════════════════════════════════════════

def draw_moe(ax):
    ax.set_xlim(0, 17); ax.set_ylim(0, 12); ax.axis("off")
    ax.set_title("MorphSparseMoE Module", fontsize=14, fontweight="bold", color=BK, pad=6)

    inp = rb(ax, 0.3, 8.5, 1.9, 1.3, r"$X{\in}\mathbb{R}^{C{\times}H{\times}W}$", KF, KE, fs=10)

    gr  = rb(ax, 0.4, 6.2, 1.3, 0.6, "GAP", TF, TE, fs=10, bold=True)
    ml1 = rb(ax, 0.25, 5.2, 1.6, 0.65, "MLP\nSiLU", TF, TE, fs=9)
    ml2 = rb(ax, 0.25, 4.25, 1.6, 0.65, "Linear", TF, TE, fs=9)
    sm  = rb(ax, 0.2, 3.25, 1.7, 0.6, r"Softmax\n$r{\in}\Delta^4$", TF, TE, fs=8.5)
    tk  = rb(ax, 0.15, 2.1, 1.8, 0.75, r"top-$k{=}2$\nmask+renorm\n$r'$", RF, RE, fs=8)

    ar(ax, 1.05, 8.5, 1.05, 6.8, lw=0.85)
    ar(ax, 1.05, 6.2, 1.05, 5.85, lw=0.85)
    ar(ax, 1.05, 5.2, 1.05, 4.9, lw=0.85)
    ar(ax, 1.05, 4.25, 1.05, 3.85, lw=0.85)
    ar(ax, 1.05, 3.25, 1.05, 2.85, lw=0.85)
    ax.text(1.05, 1.4, "Router", fontsize=10, color=TE, ha="center", fontweight="bold")

    einfo = [
        ("E0: Horizontal-Line", r"DW $1{\times}5$", "(transverse crack)", OF, OE),
        ("E1: Vertical-Line",   r"DW $5{\times}1$", "(longitudinal crack)", "#FEF3C7", "#D97706"),
        ("E2: Isotropic",       r"DW $3{\times}3$", "(oblique / short)", "#FCE7F3", "#DB2777"),
        ("E3: Region",          r"AvgPool+$1{\times}1$", "(pothole / patch)", "#E0E7FF", "#4F46E5"),
    ]
    exp = []
    ey = 9.8; eh = 1.15; eg = 0.22
    for name, ker, desc, fc, ec in einfo:
        e = rb(ax, 2.8, ey, 2.8, eh, f"{name}\n{ker}", fc, ec, fs=8.5)
        exp.append(e)
        ax.text(5.75, ey+eh/2, desc, fontsize=6.5, color=ec, ha="left", va="center", fontstyle="italic", alpha=0.85)
        ey -= (eh + eg)

    for e in exp:
        ex,ey2,ew,eh2 = e.get_bbox().bounds
        ar(ax, 2.2, 9.15, 2.8, ey2+eh2/2, lw=0.75)
    for i, e in enumerate(exp):
        ex,ey2,ew,eh2 = e.get_bbox().bounds
        rad = -0.15 if i % 2 == 0 else 0.15
        ar(ax, 1.95, 2.47, 2.8, ey2+eh2/2, c=RE, lw=0.8, cs=f"arc3,rad={rad}")

    comb = rb(ax, 6.2, 5.3, 2.8, 0.9, r"$Y{=}\sum_{i{=}0}^{3}\,r'_i{\cdot}{\rm E}_i(X)$", OF, OE, fs=9)
    prj = rb(ax, 6.5, 4.1, 2.2, 0.75, r"Conv $1{\times}1$", GF, GE, fs=10)

    for e in exp:
        ex,ey2,ew,eh2 = e.get_bbox().bounds
        ar(ax, ex+ew, ey2+eh2/2, 6.2, 5.75, lw=0.75)
    ar(ax, 7.6, 5.3, 7.6, 4.85, lw=0.95)

    ad  = rb(ax, 9.2, 4.3, 0.7, 0.7, "$+$", GF, GE, fs=14, bold=True)
    ot  = rb(ax, 10.3, 4.05, 2.0, 1.2, r"$Y_{\rm out}$\nOutput", GF, GE, fs=11, bold=True)

    ar(ax, 8.7, 4.47, 9.2, 4.65, lw=0.95)
    ar(ax, 2.2, 9.15, 9.2, 4.65, c=RE, lw=0.95, cs="arc3,rad=0.22")
    ar(ax, 9.9, 4.65, 10.3, 4.65, lw=0.95)

    ax.annotate("", xy=(7.6, 2.3), xytext=(7.6, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=RE, lw=1.0))
    ax.text(7.6, 1.95, "Only top-2 experts activated\n(sparse conditional computation)",
            fontsize=8, color=RE, ha="center", fontstyle="italic")

    lbl(ax, "b", 0.5, 11.4)


# ══════════════════════════════════════════════════════════════════════════════
#  (c) SPPF-CSPC + ECA
# ══════════════════════════════════════════════════════════════════════════════

def draw_sppf_cspc(ax):
    ax.set_xlim(0, 17); ax.set_ylim(0, 12); ax.axis("off")
    ax.set_title("SPPF-CSPC + ECA Module", fontsize=14, fontweight="bold", color=BK, pad=6)

    inp = rb(ax, 0.3, 7.5, 1.9, 1.2, r"$X{\in}\mathbb{R}^{C{\times}H{\times}W}$", KF, KE, fs=10)
    ax.text(1.25, 9.0, "CSP Split", fontsize=10, color=KE, ha="center", fontweight="bold")

    c1a = rb(ax, 2.8, 9.0, 1.6, 0.7, r"Conv $1{\times}1$", PF, PE, fs=10)
    c3a = rb(ax, 2.8, 7.9, 1.6, 0.7, r"Conv $3{\times}3$", PF, PE, fs=10)

    ar(ax, 2.2, 8.1, 2.8, 9.35, lw=0.85)
    ar(ax, 3.6, 9.0, 3.6, 8.6, lw=0.85)

    mps = []; my = 6.6
    for lb in [r"MaxPool $k{=}5$ #1", r"MaxPool $k{=}5$ #2", r"MaxPool $k{=}5$ #3"]:
        mp = rb(ax, 2.8, my, 1.6, 0.65, lb, PF, PE, fs=8)
        mps.append(mp); my -= 0.95

    ar(ax, 3.6, 7.9, 3.6, 7.25, lw=0.85)
    ar(ax, 3.6, 6.6, 3.6, 5.85, lw=0.85)
    ar(ax, 3.6, 5.65, 3.6, 4.45, lw=0.85)

    catm = rb(ax, 2.5, 2.4, 1.9, 0.6, "Concat\n(all stages)", PF, PE, fs=8.5)
    prm = rb(ax, 2.5, 1.5, 1.9, 0.65, r"Conv $1{\times}1$", PF, PE, fs=10)

    ar(ax, 3.6, 7.9, 2.8, 2.7, lw=0.75)
    ar(ax, 3.6, 6.92, 3.0, 2.7, lw=0.75)
    ar(ax, 3.6, 5.97, 3.2, 2.7, lw=0.75)
    ar(ax, 3.6, 5.02, 3.4, 2.7, lw=0.75)
    ar(ax, 3.45, 2.4, 3.45, 2.15, lw=0.95)

    sc = rb(ax, 2.8, 10.0, 1.6, 0.7, r"Conv $1{\times}1$\n(shortcut)", KF, KE, fs=9)
    ar(ax, 2.2, 8.1, 2.8, 10.35, lw=0.85)

    ccat = rb(ax, 5.3, 5.3, 1.7, 0.75, "Concat\nCSP merge", GF, GE, fs=9)
    ccnv = rb(ax, 5.3, 4.2, 1.7, 0.75, r"Conv $1{\times}1$", GF, GE, fs=10)

    ar(ax, 4.4, 1.82, 5.3, 5.67, lw=0.95)
    ar(ax, 4.4, 10.35, 5.3, 5.67, lw=0.95)
    ar(ax, 6.15, 5.3, 6.15, 4.95, lw=0.95)

    ega = rb(ax, 7.6, 6.0, 1.35, 0.6, "GAP", TF, TE, fs=10, bold=True)
    ec1 = rb(ax, 7.5, 4.9, 1.55, 0.65, r"Conv1D\n$k$(adaptive)", TF, TE, fs=8)
    esg = rb(ax, 7.6, 4.0, 1.35, 0.6, r"$\sigma$", TF, TE, fs=12, bold=True)
    emu = rb(ax, 7.4, 2.9, 1.75, 0.7, r"$\odot$\nre-weight", TF, TE, fs=9)

    ar(ax, 6.15, 4.57, 7.6, 6.3, lw=0.85)
    ar(ax, 8.27, 4.57, 8.27, 5.55, lw=0.85)
    ar(ax, 8.27, 6.0, 8.27, 5.55, lw=0.85)
    ar(ax, 8.27, 4.9, 8.27, 4.6, lw=0.85)
    ar(ax, 8.27, 4.0, 8.27, 3.6, lw=0.85)

    out = rb(ax, 9.8, 4.0, 2.2, 1.1, r"$X_{\rm out}$\nOutput\n(multi-scale)", GF, GE, fs=11, bold=True)

    ar(ax, 7.0, 4.57, 9.8, 4.55, lw=0.95)
    ar(ax, 11.0, 3.6, 11.0, 4.55, lw=0.95)

    ax.text(3.45, 0.75, "Sequential MaxPooling\n(receptive field expansion)",
            fontsize=8, color=PE, ha="center", fontstyle="italic")
    ax.text(8.27, 2.1, r"ECA: $k{=}|(\log_2 C{+}1)/2|_{\rm odd}$",
            fontsize=8, color=TE, ha="center", fontstyle="italic")

    lbl(ax, "c", 0.5, 11.4)


# ── Main ──────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(20, 7.5), dpi=300)
fig.patch.set_facecolor(WT)
draw_fdde(axes[0])
draw_moe(axes[1])
draw_sppf_cspc(axes[2])
fig.tight_layout(w_pad=1.8)

out_pdf = r"D:\Claude program\IEEE ACCESS_latex\figure2_modules.pdf"
out_png = r"D:\Claude program\IEEE ACCESS_latex\figure2_modules.png"
fig.savefig(out_pdf, bbox_inches="tight", pad_inches=0.1, format="pdf")
fig.savefig(out_png, bbox_inches="tight", pad_inches=0.1, format="png", dpi=300)
print(f"[OK] {out_pdf}")
print(f"[OK] {out_png}")
plt.close(fig)
