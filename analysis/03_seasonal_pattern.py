"""
Figure 3 — Seasonal Pattern: Monthly Heatmap + Seasonal Index
Outputs: fig3_seasonal_pattern.png, table3_seasonal_index.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "raw"
FIG_DIR = ROOT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
MONTH_SHORT = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "dengue_monthly_national.csv")
df["month"] = pd.Categorical(df["month"], categories=MONTH_ORDER, ordered=True)
df = df.sort_values(["year", "month_num"]).reset_index(drop=True)

pivot = df.pivot(index="year", columns="month_num", values="dengue_cases").fillna(0)
pivot.columns = MONTH_SHORT

# ── Seasonal index: each month's average as % of annual total ─────────────────
monthly_avg = pivot.mean(axis=0)
seasonal_index = (monthly_avg / monthly_avg.sum() * 100).round(1)

# ── Figure: two-panel ─────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), gridspec_kw={"height_ratios": [1.6, 1]})

# ── Panel 1: Heatmap ──────────────────────────────────────────────────────────
data_matrix = pivot.values.astype(float)
# Normalize row-wise (each year = 0–100%)
row_totals = data_matrix.sum(axis=1, keepdims=True)
row_totals[row_totals == 0] = 1
data_pct = data_matrix / row_totals * 100

im = ax1.imshow(data_pct, cmap="YlOrRd", aspect="auto", vmin=0, vmax=data_pct.max())

# Cell annotations
for i in range(data_pct.shape[0]):
    for j in range(data_pct.shape[1]):
        raw = int(data_matrix[i, j])
        pct = data_pct[i, j]
        color = "white" if pct > 18 else "#2C3E50"
        ax1.text(j, i, f"{raw:,}\n({pct:.0f}%)", ha="center", va="center",
                 fontsize=6.5, color=color)

ax1.set_xticks(range(12))
ax1.set_xticklabels(MONTH_SHORT, fontsize=9)
ax1.set_yticks(range(len(pivot.index)))
ax1.set_yticklabels([str(y) for y in pivot.index], fontsize=9)
ax1.set_title("Monthly Distribution of Admitted Dengue Cases by Year (%  of annual total)",
              fontsize=11, fontweight="bold", pad=8)

cbar = plt.colorbar(im, ax=ax1, orientation="vertical", pad=0.01, shrink=0.9)
cbar.set_label("% of Annual Cases", fontsize=8)

# Highlight peak months
for i in range(len(pivot.index)):
    peak_col = int(np.argmax(data_pct[i]))
    rect = plt.Rectangle((peak_col - 0.5, i - 0.5), 1, 1,
                          fill=False, edgecolor="#2C3E50", lw=2)
    ax1.add_patch(rect)

# ── Panel 2: Seasonal Index bar chart ────────────────────────────────────────
bar_colors = ["#E74C3C" if v == seasonal_index.max() else "#3498DB" for v in seasonal_index]
bars = ax2.bar(MONTH_SHORT, seasonal_index, color=bar_colors, edgecolor="white", zorder=3)

for bar, val in zip(bars, seasonal_index):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
             f"{val}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#2C3E50")

ax2.set_ylabel("Average % of Annual Cases", fontsize=10)
ax2.set_title("Seasonal Index: Average Monthly Share of Annual Dengue Burden (2023–2025)",
              fontsize=10, fontweight="bold", pad=6)
ax2.set_ylim(0, seasonal_index.max() * 1.2)
ax2.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax2.spines[["top", "right"]].set_visible(False)

# Shade Jun–Sep
for i, m in enumerate(MONTH_SHORT):
    if m in ["Jun", "Jul", "Aug", "Sep", "Oct"]:
        ax2.axvspan(i - 0.5, i + 0.5, alpha=0.09, color="#E67E22")

plt.tight_layout(pad=2)
out = FIG_DIR / "fig3_seasonal_pattern.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ── Table 3 ───────────────────────────────────────────────────────────────────
table = pd.DataFrame({
    "Month": MONTH_SHORT,
    "Avg Cases (2023-2025)": monthly_avg.values.round(0).astype(int),
    "Seasonal Index (%)": seasonal_index.values,
})
out_csv = FIG_DIR / "table3_seasonal_index.csv"
table.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")
print(table.to_string(index=False))
