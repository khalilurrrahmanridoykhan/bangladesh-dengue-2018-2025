"""
Figure 1 — Annual Dengue Trend in Bangladesh (2018–2026)
Outputs: fig1_annual_trend.png, table1_annual_summary.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "raw"
FIG_DIR = ROOT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "dengue_annual_national.csv")
df = df[df["year"] <= 2025].copy()   # exclude partial 2026
df = df.sort_values("year").reset_index(drop=True)

# ── Derived columns ────────────────────────────────────────────────────────────
df["yoy_change_pct"] = df["dengue_cases"].pct_change() * 100
df["label"] = df["dengue_cases"].apply(lambda x: f"{x:,}")

# ── Colors ─────────────────────────────────────────────────────────────────────
# Red for 2023 (record), light blue for COVID dip 2020, steel blue for rest
colors = []
for yr in df["year"]:
    if yr == 2023:
        colors.append("#C0392B")   # record year — red
    elif yr == 2020:
        colors.append("#85C1E9")   # COVID dip — light blue
    else:
        colors.append("#2980B9")   # standard — blue

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.bar(df["year"].astype(str), df["dengue_cases"],
              color=colors, edgecolor="white", linewidth=0.8, zorder=3)

# Case labels above each bar
for bar, label in zip(bars, df["label"]):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3000,
            label, ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#2C3E50")

# Annotations
ax.annotate("Record outbreak\n321,017 cases",
            xy=(df[df["year"] == 2023].index[0], 321017),
            xytext=(df[df["year"] == 2023].index[0] - 0.8, 290000),
            fontsize=8.5, color="#C0392B",
            arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.3))

ax.annotate("COVID-19\nlockdown",
            xy=(df[df["year"] == 2020].index[0], 1405),
            xytext=(df[df["year"] == 2020].index[0] + 0.4, 55000),
            fontsize=8.5, color="#2471A3",
            arrowprops=dict(arrowstyle="->", color="#2471A3", lw=1.3))

# Formatting
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Admitted Dengue Cases", fontsize=11)
ax.set_title("Annual Admitted Dengue Cases in Bangladesh (2018–2025)\nSource: DGHS HEOC Dashboard",
             fontsize=12, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, df["dengue_cases"].max() * 1.18)
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.spines[["top", "right"]].set_visible(False)

# Legend patches
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2980B9", label="Annual cases"),
    Patch(facecolor="#C0392B", label="Record year (2023)"),
    Patch(facecolor="#85C1E9", label="COVID-19 impact (2020)"),
]
ax.legend(handles=legend_elements, loc="upper left", fontsize=9, framealpha=0.8)

plt.tight_layout()
out = FIG_DIR / "fig1_annual_trend.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# ── Table 1 ────────────────────────────────────────────────────────────────────
table = df[["year", "dengue_cases", "yoy_change_pct"]].copy()
table.columns = ["Year", "Admitted Cases", "YoY Change (%)"]
table["YoY Change (%)"] = table["YoY Change (%)"].round(1)
out_csv = FIG_DIR / "table1_annual_summary.csv"
table.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")
print(table.to_string(index=False))
