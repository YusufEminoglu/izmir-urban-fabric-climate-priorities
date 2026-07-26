"""
Canonical figure style for the Izmir morphometrics manuscript.

Single source of truth for colour so the whole manuscript reads as one visual
system. Anchored on the Supplementary Fig. S2 palette (muted gold / sage /
lilac / warm-grey on a slate neutral ramp, red accent).

Usage in any figure script:

    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _manuscript_style import (apply_style, CLUSTER_PAL, STRATA_PAL,
                                    ACCENT, GOLD, NEUTRAL, CMAP_SEQ, CMAP_DIV,
                                    CMAP_GREEN, CMAP_LILAC, CMAP_HEAT, panel, tidy)
    apply_style()

Journals require figures WITHOUT an internal title (the caption carries the
message). Use panel letters (a, b, c ...) only.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

GOLD        = "#E9B420"
SAGE        = "#A0CBBF"
LILAC       = "#C5AFD5"
WARMGREY    = "#8E8E8D"
GOLDENROD   = "#B8860B"
ROSE        = "#DDB5B5"
WHEAT       = "#EBCB9C"
TERRACOTTA  = "#DEA6A3"
ACCENT      = "#DC2626"

NEUTRAL = {
    "ink":   "#1e293b", "label": "#334155", "tick":  "#475569",
    "muted": "#64748B", "soft":  "#94A3B8", "faint": "#CBD5E1",
    "panel": "#ffffff", "fig":   "#ffffff",
}

CLUSTER_PAL = {1: GOLD, 2: WARMGREY, 4: LILAC, 3: SAGE}
CLUSTER_NAMES = {1: "Compact mid-rise core", 2: "Coarse-grain large-footprint",
                 4: "Low-density peripheral", 3: "Sparse low-rise fringe"}

STRATA_PAL = {
    "waterfront_transformation": SAGE, "historic_core": GOLD,
    "peripheral_expansion": LILAC, "industrial_logistics": WARMGREY,
    "apartment_block": WHEAT, "hillside_incremental": TERRACOTTA,
    "grid_residential": ROSE,
}
QUAL = [GOLD, SAGE, LILAC, WARMGREY, GOLDENROD, TERRACOTTA, ROSE, WHEAT]

CMAP_SEQ   = LinearSegmentedColormap.from_list("ms_seq",   ["#FFF8E7", "#F3D98B", GOLD, GOLDENROD, "#6E4E06"], N=256)
CMAP_GREEN = LinearSegmentedColormap.from_list("ms_green", ["#F2F7F4", "#CFE4DA", SAGE, "#5E9384", "#2F5B4E"], N=256)
CMAP_DIV   = LinearSegmentedColormap.from_list("ms_div",   ["#2F5B4E", SAGE, "#F5F0E6", "#E8A08C", ACCENT], N=256)
CMAP_LILAC = LinearSegmentedColormap.from_list("ms_lilac", ["#F6F1F9", "#E0CEE9", LILAC, "#9B7BB0", "#5E4373"], N=256)
CMAP_HEAT  = LinearSegmentedColormap.from_list("ms_heat",  ["#FFF8E7", WHEAT, GOLD, TERRACOTTA, "#B5453A"], N=256)

for _n, _c in [("ms_seq", CMAP_SEQ), ("ms_green", CMAP_GREEN), ("ms_div", CMAP_DIV),
               ("ms_lilac", CMAP_LILAC), ("ms_heat", CMAP_HEAT)]:
    try:
        matplotlib.colormaps.register(_c, name=_n, force=True)
    except Exception:
        pass


def apply_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "text.color": NEUTRAL["ink"], "axes.labelcolor": NEUTRAL["label"],
        "axes.edgecolor": NEUTRAL["muted"], "axes.titlecolor": NEUTRAL["ink"],
        "xtick.color": NEUTRAL["tick"], "ytick.color": NEUTRAL["tick"],
        "axes.facecolor": NEUTRAL["panel"], "figure.facecolor": NEUTRAL["fig"],
        "savefig.facecolor": NEUTRAL["fig"],
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": NEUTRAL["faint"],
        "grid.linewidth": 0.6, "grid.alpha": 0.7, "axes.linewidth": 0.9,
        "font.size": 10.5, "axes.labelsize": 11, "axes.titlesize": 11.5,
        "xtick.labelsize": 9.5, "ytick.labelsize": 9.5, "legend.fontsize": 9.5,
        "legend.frameon": False, "figure.dpi": 110, "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def panel(ax, letter, dx=-0.02, dy=1.03, fontsize=13, weight="bold"):
    ax.text(dx, dy, f"({letter})", transform=ax.transAxes, fontsize=fontsize,
            fontweight=weight, color=NEUTRAL["ink"], ha="right", va="bottom")


def tidy(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(NEUTRAL["muted"]); ax.spines[s].set_linewidth(0.9)
    return ax
