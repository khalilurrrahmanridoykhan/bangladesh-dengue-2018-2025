"""
Figure 4 — Division-Level Dengue Burden (2026 YTD)
Outputs: fig4_division_analysis.png, table4_division_incidence.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/khalilur/Documents/AIWORK/dengue/data/raw")
FIG_DIR  = Path("/Users/khalilur/Documents/AIWORK/dengue/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# BBS 2022 Census division populations
POPULATION = {
    "Dhaka":      36054418,
    "Chattogram": 28423019,
    "Rajshahi":   18484858,
    "Khulna":     15563000,
    "Barishal":    8325666,
    "Sylhet":     10009239,
    "Rangpur":    15665000,
    "Mymensingh": 11370000,
}

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "dengue_division_2026.csv")
# Keep only 8 main divisions — drop city corporation duplicates
valid_divs = list(POPULATION.keys())
df = df[df["division"].isin(valid_divs)].copy()
df = df.sort_values("dengue_cases_cumulative", ascending=False).reset_index(drop=True)

# Add population and incidence rate per 100k
df["population"] = df["division"].map(POPULATION)
df["incidence_per_100k"] = (df["dengue_cases_cumulative"] / df["population"] * 100000).round(2)
df["cfr_pct"] = (df["dengue_deaths_cumulative"] / df["dengue_cases_cumulative"] * 100).round(2)

# ── Weekly division trends ─────────────────────────────────────────────────────
dw = pd.read_csv(DATA_DIR / "dengue_weekly_division_2026.csv")
# Normalise division names
dw["division"] = dw["division"].replace({"Barisal": "Barishal"})
dw = dw[dw["division"].isin(valid_divs)]

# ── Figure: two-panel ─────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 7))
gs = gridspec.GridSpec(1, 2, width_ratios=[1.2, 1.8], wspace=0.35)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ── Left panel: incidence per 100k horizontal bars ───────────────────────────
df_sorted = df.sort_values("incidence_per_100k", ascending=True)
bar_colors = ["#C0392B" if v == df_sorted["incidence_per_100k"].max()
              else "#2980B9" for v in df_sorted["incidence_per_100k"]]

bars = ax1.barh(df_sorted["division"], df_sorted["incidence_per_100k"],
                color=bar_colors, edgecolor="white", height=0.65, zorder=3)

for bar, val, raw in zip(bars, df_sorted["incidence_per_100k"], df_sorted["dengue_cases_cumulative"]):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}  ({raw:,} cases)",
             va="center", fontsize=8, color="#2C3E50")

ax1.set_xlabel("Incidence per 100,000 population", fontsize=10)
ax1.set_title("Dengue Incidence Rate\nby Division (2026 YTD)", fontsize=10,
              fontweight="bold", pad=8)
ax1.set_xlim(0, df_sorted["incidence_per_100k"].max() * 1.55)
ax1.grid(axis="x", linestyle="--", alpha=0.4, zorder=0)
ax1.spines[["top", "right"]].set_visible(False)

# ── Right panel: weekly trends by division ────────────────────────────────────
COLORS = ["#C0392B","#2980B9","#27AE60","#E67E22","#8E44AD","#17A589","#F39C12","#1A5276"]
top_divs = df.sort_values("dengue_cases_cumulative", ascending=False)["division"].tolist()

for i, div in enumerate(top_divs):
    sub = dw[dw["division"] == div].sort_values("week_num")
    if sub.empty:
        continue
    lw = 2.2 if i < 3 else 1.3
    alpha = 1.0 if i < 3 else 0.6
    ax2.plot(sub["week_num"], sub["dengue_cases"],
             label=div, color=COLORS[i % len(COLORS)],
             lw=lw, alpha=alpha, marker="o", markersize=3)

ax2.set_xlabel("Epidemiological Week (2026)", fontsize=10)
ax2.set_ylabel("Admitted Cases (weekly)", fontsize=10)
ax2.set_title("Weekly Dengue Cases by Division\n(2026, Weeks 1–22)", fontsize=10,
              fontweight="bold", pad=8)
ax2.legend(fontsize=8, ncol=2, loc="upper right", framealpha=0.85)
ax2.grid(linestyle="--", alpha=0.35, zorder=0)
ax2.spines[["top", "right"]].set_visible(False)

fig.suptitle("Geographic Distribution of Dengue in Bangladesh (2026 YTD)\nSource: DGHS HEOC Dashboard",
             fontsize=12, fontweight="bold", y=1.01)

plt.tight_layout()
out = FIG_DIR / "fig4_division_analysis.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ── Table 4 ───────────────────────────────────────────────────────────────────
table = df[["division","dengue_cases_cumulative","dengue_deaths_cumulative",
            "population","incidence_per_100k","cfr_pct"]].copy()
table.columns = ["Division","Cases (2026 YTD)","Deaths (2026 YTD)",
                 "Population (2022)","Incidence per 100k","CFR (%)"]
out_csv = FIG_DIR / "table4_division_incidence.csv"
table.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")
print(table.to_string(index=False))
