"""
Figure 13 — Alluvial (Sankey) transition flow:
a-priori fabric strata -> morphometric clusters -> TOPSIS priority tiers.

Node heights are the true cell counts of the full census (N = 3,777); the three
columns are vertically centred so the ribbons align with the bars. Cluster IDs
are mapped to the four interpretive super-types by their morphometric profile
(cluster_profiles.csv), matching the manuscript description.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
CLUST_PATH = os.path.join(PROJ, "data", "03_processed", "cell_clusters.csv")
PRIO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_priority.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "flow_sankey.png")

df = pd.merge(pd.read_csv(CLUST_PATH), pd.read_csv(PRIO_PATH),
              on=["sample_id", "stratum_name", "x", "y"])

# cluster id -> interpretive super-type (by profile: see cluster_profiles.csv)
#   1: FAR 1.44, compact            2: largest footprint, hottest (coarse/industrial)
#   3: n=123, sparse low-rise        4: FAR 0.12, high green (low-density peripheral)
cluster_labels = {1: "Compact core", 2: "Coarse-grain / industrial",
                  3: "Sparse low-rise fringe", 4: "Low-density peripheral"}
df["cluster_label"] = df["cluster"].map(cluster_labels)
assert df["cluster_label"].notna().all(), "unmapped cluster id present"


def get_tier(rank):
    return "High priority" if rank <= 233 else ("Medium priority" if rank <= 466 else "Low priority")


df["priority_tier"] = df["rank_mean"].apply(get_tier)

strata_order = ["historic_core", "apartment_block", "waterfront_transformation",
                "hillside_incremental", "grid_residential", "industrial_logistics",
                "peripheral_expansion"]
strata_labels = {"historic_core": "Historic Core", "apartment_block": "Apartment Block",
                 "waterfront_transformation": "Waterfront Trans.", "hillside_incremental": "Hillside / Inc.",
                 "grid_residential": "Grid Res.", "industrial_logistics": "Industrial / Log.",
                 "peripheral_expansion": "Peripheral Exp."}
clusters_order = ["Compact core", "Coarse-grain / industrial",
                  "Low-density peripheral", "Sparse low-rise fringe"]
priority_order = ["Low priority", "Medium priority", "High priority"]

colors_strata = {"historic_core": "#E9B420", "grid_residential": "#DDB5B5", "apartment_block": "#EBCB9C",
                 "waterfront_transformation": "#A0CBBF", "hillside_incremental": "#DEA6A3",
                 "industrial_logistics": "#8E8E8D", "peripheral_expansion": "#C5AFD5"}
colors_clusters = {"Compact core": "#E9B420", "Coarse-grain / industrial": "#8E8E8D",
                   "Low-density peripheral": "#C5AFD5", "Sparse low-rise fringe": "#A0CBBF"}
colors_priority = {"High priority": "#DEA6A3", "Medium priority": "#EBCB9C", "Low priority": "#CBD5E1"}

flow1 = df.groupby(["stratum_name", "cluster_label"]).size().unstack(fill_value=0)
flow2 = df.groupby(["cluster_label", "priority_tier"]).size().unstack(fill_value=0)

plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"], "text.color": "#1e293b"})

# ── geometry ──────────────────────────────────────────────────────────────────
X_POS = [1.0, 2.5, 4.0]
CW = 0.16
N = len(df)
GAP = 0.030 * N


def stack(order, counts, H):
    total = sum(counts[k] for k in order) + GAP * (len(order) - 1)
    y = H / 2 + total / 2
    pos = {}
    for k in order:
        h = counts[k]
        pos[k] = {"start": y - h, "end": y, "height": h}
        y -= h + GAP
    return pos


strata_counts = {s: int((df["stratum_name"] == s).sum()) for s in strata_order}
cluster_counts = {c: int((df["cluster_label"] == c).sum()) for c in clusters_order}
priority_counts = {p: int((df["priority_tier"] == p).sum()) for p in priority_order}

H = max(sum(strata_counts.values()) + GAP * 6,
        sum(cluster_counts.values()) + GAP * 3,
        sum(priority_counts.values()) + GAP * 2)

pos0 = stack(strata_order, strata_counts, H)
pos1 = stack(clusters_order, cluster_counts, H)
pos2 = stack(priority_order, priority_counts, H)

fig, ax = plt.subplots(figsize=(13, 9), facecolor="#ffffff")
ax.axis("off")


def node_bars(order, pos, x, colors, labelmap, side):
    for k in order:
        p = pos[k]
        ax.add_patch(patches.Rectangle((x - CW / 2, p["start"]), CW, p["height"],
                                       facecolor=colors[k], edgecolor="#475569", linewidth=0.5, alpha=0.95))
        nm = labelmap[k] if isinstance(labelmap, dict) else k
        txt = f"{nm}\n(n = {p['height']:,})"
        bbox = dict(boxstyle="round,pad=0.2", fc="#ffffffd9", ec="none")
        if side == "left":
            ax.text(x - CW / 2 - 0.06, (p["start"] + p["end"]) / 2, txt, ha="right", va="center",
                    fontsize=8.5, fontweight="bold", color="#1e293b", bbox=bbox, zorder=5)
        else:
            ax.text(x + CW / 2 + 0.06, (p["start"] + p["end"]) / 2, txt, ha="left", va="center",
                    fontsize=8.5, fontweight="bold", color="#1e293b", bbox=bbox, zorder=5)


node_bars(strata_order, pos0, X_POS[0], colors_strata, strata_labels, "left")
node_bars(clusters_order, pos1, X_POS[1], colors_clusters, {c: c for c in clusters_order}, "left")
node_bars(priority_order, pos2, X_POS[2], colors_priority, {p: p for p in priority_order}, "right")


def ribbon(x0, x1, y0, y1, h, color):
    dx = (x1 - x0) * 0.42
    verts = [(x0, y0), (x0 + dx, y0), (x1 - dx, y1), (x1, y1),
             (x1, y1 + h), (x1 - dx, y1 + h), (x0 + dx, y0 + h), (x0, y0 + h), (x0, y0)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    ax.add_patch(patches.PathPatch(Path(verts, codes), facecolor=color, alpha=0.32, edgecolor="none"))


def draw_flows(order_src, order_dst, flow, pos_src, pos_dst, xs, xd, colors_src):
    out_off = {k: pos_src[k]["start"] for k in order_src}
    in_off = {k: pos_dst[k]["start"] for k in order_dst}
    for k in order_dst:                      # fill destinations in column order
        for s in order_src:
            if k not in flow.columns or s not in flow.index:
                continue
            f = int(flow.loc[s, k])
            if f <= 0:
                continue
            ribbon(xs + CW / 2, xd - CW / 2, out_off[s], in_off[k], f, colors_src[s])
            if f >= 15:
                xm = xs + 0.32 * (xd - xs)
                ym = 0.68 * (out_off[s] + f / 2) + 0.32 * (in_off[k] + f / 2)
                ax.text(xm, ym, f"{f:,}", ha="center", va="center", fontsize=7,
                        color="#334155", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.12", fc="#ffffffcc", ec="none"))
            out_off[s] += f
            in_off[k] += f


draw_flows(strata_order, clusters_order, flow1, pos0, pos1, X_POS[0], X_POS[1], colors_strata)
draw_flows(clusters_order, priority_order, flow2, pos1, pos2, X_POS[1], X_POS[2], colors_clusters)

# column headers
top = H + 0.045 * H
for x, t in zip(X_POS, ["A-priori fabric strata", "Morphometric clusters", "TOPSIS priority tiers"]):
    ax.text(x, top, t, ha="center", fontsize=11.5, fontweight="bold", color="#0f172a")

ax.set_xlim(X_POS[0] - 1.25, X_POS[2] + 1.25)
ax.set_ylim(-0.05 * H, H + 0.12 * H)

fig.suptitle("Fabric-resilience transition flow — strata → clusters → priority", fontsize=14.5,
             fontweight="bold", color="#0f172a", y=0.975)
fig.text(0.5, 0.93, f"Full urban census (N = {N:,}); ribbons < 15 cells left unlabeled",
         ha="center", va="center", fontsize=10, color="#475569")
fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)
fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Successfully generated alluvial diagram: {OUT_FIG}")
print("cluster counts:", cluster_counts)
print("priority counts:", priority_counts)
