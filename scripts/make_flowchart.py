"""
Figure 2 — Methodological flowchart of the two-stage explain -> optimize
typomorphological urban-resilience pipeline.

Journal-quality layout: phase rail + swimlane bands that make the
explain -> optimize narrative explicit, auto-sized boxes with left-aligned
bullets, fork/merge elbow connectors, 300 dpi, style-guide palette.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "methodology_flowchart.png")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
})

# ── palette (style guide) ─────────────────────────────────────────────────────
INK     = "#1E293B"
LABEL   = "#334155"
ARROW   = "#64748B"
FACE    = "#ffffff"

PHASES = {  # band tint, accent bar colour, rail label
    "INPUTS":     ("#F4F6F8", "#8E8E8D", "Open data"),
    "FOUNDATION": ("#EFF6F4", "#A0CBBF", "Morphometric foundation"),
    "EXPLAIN":    ("#FBF3F2", "#DEA6A3", "Stage I · Explain"),
    "OPTIMISE":   ("#FCF7EC", "#E9B420", "Stage II · Optimise"),
}

# ── content ───────────────────────────────────────────────────────────────────
BOXES = [
    dict(id="inputs", phase="INPUTS", span="full",
         face="#FFFFFF", border="#8E8E8D",
         title="Input databases (open & official)",
         lines=[
             "Street networks & buildings — municipal IMM GPKG layers",
             "High-resolution land cover — ESA WorldCover 2021 (10 m)",
             "Digital elevation & slope — Copernicus GLO-30 (30 m)",
             "Land-surface temperature — JJA Landsat mean, 2014–2024",
             "Demographic & social vulnerability — TÜİK ADNKS (mahalle)",
         ]),
    dict(id="s1", phase="FOUNDATION", span="full",
         face="#FFFCF6", border="#EBCB9C",
         title="1 · Spatial exclusions & grid framing",
         lines=[
             "250 m fishnet aligned to INSPIRE / GHSL grids",
             "Urban-fabric filter — built ≥ 0.10, water ≤ 0.50, slope ≤ 15 %",
             "Exclusions reduce 16,496 in-region cells → 3,777 urban cells",
         ]),
    dict(id="s2", phase="FOUNDATION", span="full",
         face="#F4FAF8", border="#A0CBBF",
         title="2 · Full-census morphometric cross-attribution",
         lines=[
             "Full census — 3,777 retained urban cells, 7 a-priori strata",
             "Morphological tessellation (plot proxy) & street planarisation",
             "29 morphometric, network, contextual & hazard indicators",
             "Cross-attribution to 250 m grid (400 / 800 m service areas)",
         ]),
    dict(id="s3", phase="EXPLAIN", span="left",
         face="#FDF6F5", border="#DEA6A3",
         title="3 · Explain — heat-mechanism attribution",
         lines=[
             "Predict measured summer LST from indicators",
             "XGBoost with spatial-block cross-validation",
             "6 k-means coordinate blocks (GroupKFold)",
             "TreeSHAP global & local attribution",
             "Per-stratum signed heat-mechanism map",
         ]),
    dict(id="s4", phase="EXPLAIN", span="right",
         face="#FCFAFD", border="#C5AFD5",
         title="4 · Typology — fabric clustering & scale",
         lines=[
             "PCA reduction (91 % variance explained)",
             "Ward hierarchical clustering (k = 4 super-types)",
             "Re-cluster at 500 m to test resolution stability",
             "Spatial scale-agreement validation (ARI = 0.38)",
         ]),
    dict(id="s5", phase="OPTIMISE", span="full",
         face="#FFFBF0", border="#E9B420",
         title="5 · Optimise — spatial statistics & MCDA prioritisation",
         lines=[
             "Spatial diagnostics — global Moran's I, LISA, Getis-Ord Gi*",
             "Priority vectors — heat, cooling deficit, access deficit, coastal exposure, SVI",
             "Pareto screen — 223 non-dominated cells of 3,777",
             "TOPSIS sorting & Monte-Carlo robustness (2,000 Dirichlet runs)",
         ]),
]

# ── geometry ──────────────────────────────────────────────────────────────────
W = 12.4
FX, FW = 1.45, 9.55           # full-width box
LX, LW = 1.45, 4.65           # left parallel box
RX, RW = 6.35, 4.65           # right parallel box
BAND_X0, BAND_X1 = 0.18, 11.78
GAP = 0.62
LINE_H = 0.275
TITLE_H = 0.56
PAD_B = 0.20


def box_h(b):
    return TITLE_H + len(b["lines"]) * LINE_H + PAD_B


# layout pass (top-down) -------------------------------------------------------
total_h = 0.0
i = 0
while i < len(BOXES):
    if BOXES[i]["span"] == "left":
        total_h += max(box_h(BOXES[i]), box_h(BOXES[i + 1])) + GAP
        i += 2
    else:
        total_h += box_h(BOXES[i]) + GAP
        i += 1
H = total_h - GAP + 0.6  # trim last gap, add top/bottom margin

fig, ax = plt.subplots(figsize=(W, H), facecolor=FACE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_axis_off()

pos = {}
y = H - 0.30
i = 0
while i < len(BOXES):
    b = BOXES[i]
    if b["span"] == "left":
        b2 = BOXES[i + 1]
        h = max(box_h(b), box_h(b2))
        pos[b["id"]] = (LX, y - h, LW, h)
        pos[b2["id"]] = (RX, y - h, RW, h)
        y -= h + GAP
        i += 2
    else:
        h = box_h(b)
        pos[b["id"]] = (FX, y - h, FW, h)
        y -= h + GAP
        i += 1

# ── phase swimlane bands + rail labels ────────────────────────────────────────
phase_ids = {}
for b in BOXES:
    phase_ids.setdefault(b["phase"], []).append(b["id"])

for ph, ids in phase_ids.items():
    tint, accent, rail = PHASES[ph]
    tops = [pos[i][1] + pos[i][3] for i in ids]
    bots = [pos[i][1] for i in ids]
    y1, y0 = max(tops) + 0.16, min(bots) - 0.16
    ax.add_patch(patches.FancyBboxPatch(
        (BAND_X0, y0), BAND_X1 - BAND_X0, y1 - y0,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=tint, edgecolor="none", zorder=0))
    # left accent bar
    ax.add_patch(patches.Rectangle((BAND_X0 + 0.12, y0 + 0.08), 0.12, y1 - y0 - 0.16,
                                   facecolor=accent, edgecolor="none", zorder=1))
    # rotated rail label
    ax.text(BAND_X0 + 0.62, (y0 + y1) / 2, rail.upper(), rotation=90,
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=LABEL, zorder=1, linespacing=1.0)


# ── boxes ─────────────────────────────────────────────────────────────────────
def draw_box(b):
    x, yy, w, h = pos[b["id"]]
    ax.add_patch(patches.FancyBboxPatch(
        (x + 0.05, yy - 0.06), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor="#CBD5E1", edgecolor="none", alpha=0.45, zorder=2))
    ax.add_patch(patches.FancyBboxPatch(
        (x, yy), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=b["face"], edgecolor=b["border"], linewidth=1.4, zorder=3))
    ax.text(x + w / 2, yy + h - 0.30, b["title"], fontsize=10.5, fontweight="bold",
            ha="center", va="center", color=INK, zorder=4)
    ax.plot([x + 0.28, x + w - 0.28], [yy + h - TITLE_H + 0.07] * 2,
            color=b["border"], linewidth=1.0, zorder=4)
    ty = yy + h - TITLE_H - 0.04
    for ln in b["lines"]:
        ax.text(x + 0.30, ty, "•", fontsize=9, ha="left", va="top",
                color=b["border"], zorder=4, fontweight="bold")
        ax.text(x + 0.52, ty, ln, fontsize=9, ha="left", va="top",
                color=LABEL, zorder=4)
        ty -= LINE_H


for b in BOXES:
    draw_box(b)


# ── connectors ────────────────────────────────────────────────────────────────
def vline(x, y_from, y_to, arrow=False):
    if arrow:
        ax.annotate("", xy=(x, y_to), xytext=(x, y_from),
                    arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.6,
                                    mutation_scale=14, shrinkA=0, shrinkB=0), zorder=5)
    else:
        ax.plot([x, x], [y_from, y_to], color=ARROW, lw=1.6, zorder=5)


def hline(x0, x1, yv):
    ax.plot([x0, x1], [yv, yv], color=ARROW, lw=1.6, zorder=5)


def top_c(i): x, yy, w, h = pos[i]; return (x + w / 2, yy + h)
def bot_c(i): x, yy, w, h = pos[i]; return (x + w / 2, yy)

# inputs -> s1 -> s2
vline(*[bot_c("inputs")[0]], bot_c("inputs")[1], top_c("s1")[1], arrow=True)
vline(bot_c("s1")[0], bot_c("s1")[1], top_c("s2")[1], arrow=True)

# s2 -> fork -> s3 & s4
b2x, b2y = bot_c("s2")
jy = b2y - GAP / 2
s3x, s4x = top_c("s3")[0], top_c("s4")[0]
vline(b2x, b2y, jy)
hline(s3x, s4x, jy)
vline(s3x, jy, top_c("s3")[1], arrow=True)
vline(s4x, jy, top_c("s4")[1], arrow=True)

# s3 & s4 -> merge -> s5
s5x, s5y = top_c("s5")
mjy = s5y + GAP / 2
vline(bot_c("s3")[0], bot_c("s3")[1], mjy)
vline(bot_c("s4")[0], bot_c("s4")[1], mjy)
hline(bot_c("s3")[0], bot_c("s4")[0], mjy)
vline(s5x, mjy, s5y, arrow=True)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none",
            bbox_inches="tight", pad_inches=0.15)
plt.close()

import shutil
outputs_fig = os.path.dirname(OUT_FIG)
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(OUT_FIG, os.path.join(figs_cur, "methodology_flowchart.png"))

print(f"Successfully generated methodology flowchart: {OUT_FIG}")
