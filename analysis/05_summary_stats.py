"""
Table 5 — Key Summary Statistics for Paper (Results Section)
Outputs: table5_key_stats.csv  (all numbers ready to paste into manuscript)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

DATA_DIR = Path("/Users/khalilur/Documents/AIWORK/dengue/data/raw")
FIG_DIR  = Path("/Users/khalilur/Documents/AIWORK/dengue/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

POPULATION_BD = 169_356_251  # BBS 2022 national population

# ── Load all datasets ──────────────────────────────────────────────────────────
annual   = pd.read_csv(DATA_DIR / "dengue_annual_national.csv")
monthly  = pd.read_csv(DATA_DIR / "dengue_monthly_national.csv")
weekly   = pd.read_csv(DATA_DIR / "dengue_weekly_national.csv")
division = pd.read_csv(DATA_DIR / "dengue_division_2026.csv")

annual = annual.sort_values("year").reset_index(drop=True)

# ── Stat 1: Annual trend ───────────────────────────────────────────────────────
pre_covid  = annual[annual["year"].isin([2018, 2019])]["dengue_cases"].mean()
record_yr  = int(annual.loc[annual["dengue_cases"].idxmax(), "year"])
record_val = int(annual["dengue_cases"].max())
baseline   = int(annual[annual["year"] == 2018]["dengue_cases"].iloc[0])
fold_inc   = round(record_val / baseline, 1)

# ── Stat 2: COVID dip ─────────────────────────────────────────────────────────
covid_cases = int(annual[annual["year"] == 2020]["dengue_cases"].iloc[0])
covid_drop_pct = round((1 - covid_cases / pre_covid) * 100, 1)

# ── Stat 3: 2019 vs 2023 ──────────────────────────────────────────────────────
cases_2019 = int(annual[annual["year"] == 2019]["dengue_cases"].iloc[0])
cases_2023 = int(annual[annual["year"] == 2023]["dengue_cases"].iloc[0])
pct_inc_19_23 = round((cases_2023 - cases_2019) / cases_2019 * 100, 1)

# ── Stat 4: Seasonal peak ──────────────────────────────────────────────────────
m23 = monthly[monthly["year"] == 2023].sort_values("month_num")
peak_month_2023 = m23.loc[m23["dengue_cases"].idxmax(), "month"]
peak_month_cases = int(m23["dengue_cases"].max())
peak_month_pct   = round(peak_month_cases / cases_2023 * 100, 1)

monsoon_months = [6, 7, 8, 9, 10]  # Jun–Oct
monsoon_cases_2023 = int(m23[m23["month_num"].isin(monsoon_months)]["dengue_cases"].sum())
monsoon_pct_2023   = round(monsoon_cases_2023 / cases_2023 * 100, 1)

# ── Stat 5: Weekly peak ────────────────────────────────────────────────────────
w23 = weekly[weekly["year"] == 2023].sort_values("week_num")
peak_week_2023  = w23.loc[w23["dengue_cases"].idxmax(), "week"]
peak_week_cases = int(w23["dengue_cases"].max())

# ── Stat 6: Post-2023 sustained burden ─────────────────────────────────────────
cases_2024 = int(annual[annual["year"] == 2024]["dengue_cases"].iloc[0])
cases_2025 = int(annual[annual["year"] == 2025]["dengue_cases"].iloc[0])
avg_24_25  = (cases_2024 + cases_2025) / 2
pct_above_baseline = round((avg_24_25 - baseline) / baseline * 100, 1)

# ── Stat 7: Trend test (Mann-Kendall approximation) ───────────────────────────
pre_2023 = annual[annual["year"] < 2023]["dengue_cases"].values
slope, intercept, r, p_val, se = stats.linregress(
    range(len(pre_2023)), pre_2023
)

# ── Stat 8: National incidence 2023 per 100k ──────────────────────────────────
incidence_2023_per100k = round(cases_2023 / POPULATION_BD * 100000, 1)
incidence_2024_per100k = round(cases_2024 / POPULATION_BD * 100000, 1)

# ── Stat 9: Division concentration 2026 ───────────────────────────────────────
VALID_DIVS = ["Dhaka","Chattogram","Rajshahi","Khulna","Barishal","Sylhet","Rangpur","Mymensingh"]
div = division[division["division"].isin(VALID_DIVS)].copy()
total_div = div["dengue_cases_cumulative"].sum()
top_div   = div.loc[div["dengue_cases_cumulative"].idxmax(), "division"]
top_div_cases = int(div["dengue_cases_cumulative"].max())
top_div_pct   = round(top_div_cases / total_div * 100, 1)

# Top 3 divisions
top3 = div.nlargest(3, "dengue_cases_cumulative")
top3_cases = int(top3["dengue_cases_cumulative"].sum())
top3_pct   = round(top3_cases / total_div * 100, 1)

# ── Build summary table ────────────────────────────────────────────────────────
rows = [
    ("Study period", "2018–2025 (annual); 2023–2025 (monthly/weekly)"),
    ("Total cases — 2018", f"{baseline:,}"),
    ("Total cases — 2019", f"{cases_2019:,}"),
    ("Total cases — 2020 (COVID)", f"{covid_cases:,}"),
    ("COVID-19 case reduction vs 2018–2019 avg", f"{covid_drop_pct}%"),
    ("Total cases — 2023 (record)", f"{cases_2023:,}"),
    ("National incidence 2023 (per 100k)", f"{incidence_2023_per100k}"),
    ("Total cases — 2024", f"{cases_2024:,}"),
    ("Total cases — 2025", f"{cases_2025:,}"),
    ("National incidence 2024 (per 100k)", f"{incidence_2024_per100k}"),
    ("Fold increase 2018→2023", f"{fold_inc}×"),
    ("% increase 2019→2023", f"{pct_inc_19_23}%"),
    ("Avg cases 2024–2025 vs 2018 baseline increase", f"+{pct_above_baseline}%"),
    ("Peak month 2023", peak_month_2023),
    ("Peak month cases 2023", f"{peak_month_cases:,} ({peak_month_pct}% of annual)"),
    ("Monsoon burden 2023 (Jun–Oct)", f"{monsoon_cases_2023:,} ({monsoon_pct_2023}% of annual)"),
    ("Peak week 2023", peak_week_2023),
    ("Peak week cases 2023", f"{peak_week_cases:,}"),
    ("Linear trend slope (pre-2023, cases/year)", f"{slope:,.0f}"),
    ("Linear trend p-value (pre-2023)", f"{p_val:.4f}"),
    ("Top division by cases 2026 YTD", f"{top_div} ({top_div_cases:,} cases, {top_div_pct}% of total)"),
    ("Top 3 divisions share 2026 YTD", f"{top3_pct}% of all division cases"),
    ("Data source", "DGHS HEOC Dengue Dashboard"),
    ("Data access date", "June 2026"),
    ("Ethics", "Publicly available aggregated data; IRB waiver applies"),
]

table = pd.DataFrame(rows, columns=["Statistic", "Value"])
out_csv = FIG_DIR / "table5_key_stats.csv"
table.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}\n")
print(table.to_string(index=False))
