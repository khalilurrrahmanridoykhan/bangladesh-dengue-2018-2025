"""
Figure 2 — Weekly Epidemic Curve Comparison (2023 vs 2024 vs 2025)
Outputs: fig2_epidemic_curve.png, table2_weekly_peaks.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/khalilur/Documents/AIWORK/dengue/data/raw")
FIG_DIR  = Path("/Users/khalilur/Documents/AIWORK/dengue/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "dengue_weekly_national.csv")
df = df.sort_values(["year", "week_num"]).reset_index(drop=True)

# Align weeks 1-52 for each year
years = sorted(df["year"].unique())
pivot = df.pivot(index="week_num", columns="year", values="dengue_cases").fillna(0)
pivot = pivot.reindex(range(1, 53)).fillna(0)

# ── Colors & styles ────────────────────────────────────────────────────────────
YEAR_STYLE = {
    2023: {"color": "#C0392B", "lw": 2.5, "ls": "-",  "label": "2023 (record: 321,017)"},
    2024: {"color": "#2980B9", "lw": 1.8, "ls": "--", "label": "2024 (101,211)"},
    2025: {"color": "#27AE60", "lw": 1.8, "ls": ":",  "label": "2025 (102,861)"},
}

# Monsoon season: weeks ~23–40 (Jun–Sep)
MONSOON_START, MONSOON_END = 23, 40

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

# Shade monsoon season
ax.axvspan(MONSOON_START, MONSOON_END, alpha=0.08, color="#E67E22", label="Monsoon season (Jun–Sep)")

for yr in years:
    if yr not in YEAR_STYLE or yr not in pivot.columns:
        continue
    s = YEAR_STYLE[yr]
    vals = pivot[yr].values
    ax.plot(pivot.index, vals, color=s["color"], lw=s["lw"],
            linestyle=s["ls"], label=s["label"], zorder=3)

    # Mark peak week
    peak_wk = int(pivot[yr].idxmax())
    peak_val = int(pivot[yr].max())
    ax.annotate(f"W{peak_wk}\n({peak_val:,})",
                xy=(peak_wk, peak_val),
                xytext=(peak_wk + 2, peak_val + peak_val * 0.06),
                fontsize=7.5, color=s["color"],
                arrowprops=dict(arrowstyle="->", color=s["color"], lw=0.9))

# X-axis: month labels at ~week midpoints
month_weeks = [1, 5, 9, 14, 18, 23, 27, 31, 36, 40, 44, 49]
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
ax.set_xticks(month_weeks)
ax.set_xticklabels(month_labels, fontsize=9)
ax.set_xlim(1, 52)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xlabel("Epidemiological Week (Month)", fontsize=11)
ax.set_ylabel("Admitted Dengue Cases (weekly)", fontsize=11)
ax.set_title("Weekly Dengue Epidemic Curves — Bangladesh 2023, 2024, 2025\nSource: DGHS HEOC Dashboard",
             fontsize=12, fontweight="bold", pad=12)
ax.legend(loc="upper left", fontsize=9, framealpha=0.85)
ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
out = FIG_DIR / "fig2_epidemic_curve.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ── Table 2 — Peak weeks ───────────────────────────────────────────────────────
rows = []
for yr in years:
    if yr not in pivot.columns:
        continue
    peak_wk  = int(pivot[yr].idxmax())
    peak_val = int(pivot[yr].max())
    total    = int(pivot[yr].sum())
    rows.append({
        "Year": yr,
        "Peak Week": f"W{peak_wk:02d}",
        "Peak Weekly Cases": peak_val,
        "Annual Total (from weekly)": total,
    })
table = pd.DataFrame(rows)
out_csv = FIG_DIR / "table2_weekly_peaks.csv"
table.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")
print(table.to_string(index=False))
