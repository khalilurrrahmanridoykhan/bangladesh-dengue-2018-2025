"""
DGHS Bangladesh — Dengue Dashboard Scraper
============================================
Source: https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php

Extracts ALL Highcharts data embedded in the dashboard page:
  - Annual national totals 2018–2026
  - Monthly national cases/deaths 2023, 2024, 2025
  - Weekly national cases/deaths 2023, 2024, 2025
  - Daily national cases 2026 (Jan–present)
  - Division-level cases + deaths 2026
  - Weekly division breakdown 2026
  - Age/gender distribution 2026

Outputs (saved to ./data/raw/):
  dengue_annual_national.csv
  dengue_monthly_national.csv
  dengue_weekly_national.csv
  dengue_daily_2026.csv
  dengue_division_2026.csv
  dengue_weekly_division_2026.csv
  dengue_scrape_log.txt

Run:  python3 scrape_dengue_dashboard.py
"""

import requests
import urllib3
import re
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DASHBOARD_URL = "https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php"
OUT_DIR = Path("/Users/khalilur/Documents/AIWORK/dengue/data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

BANGLA_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

LOG = []


# ── Fetch ──────────────────────────────────────────────────────────────────────

def fetch_dashboard() -> str:
    print("  Fetching dashboard...")
    r = requests.get(DASHBOARD_URL, headers=HEADERS, verify=False, timeout=30)
    r.raise_for_status()
    LOG.append(f"Dashboard fetch: {r.status_code}, {len(r.text)} bytes")
    return r.text


# ── Parser helpers ─────────────────────────────────────────────────────────────

def extract_chart(html: str, chart_id: str) -> dict:
    """
    Extract categories and all named series from a Highcharts.chart('chart_id', {...}) block.
    Returns: {categories: [...], series: [{name: str, data: [...]}]}
    """
    # Find the script block containing this chart id
    pattern = re.compile(
        rf"Highcharts\.chart\(['\"]?{re.escape(chart_id)}['\"]?.*?(?=Highcharts\.chart\(|</script>)",
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        return {"categories": [], "series": []}

    block = match.group(0)

    # Categories
    cats_m = re.search(r"categories\s*:\s*(\[[^\]]+\])", block)
    categories = []
    if cats_m:
        raw = cats_m.group(1)
        categories = re.findall(r'["\']([^"\']+)["\']', raw)

    # All series: name + data pairs
    series = []
    # Find each { name: '...', data: [...] } block inside series: [...]
    series_blocks = re.findall(
        r'\{[^{}]*name\s*:\s*["\']([^"\']+)["\'][^{}]*data\s*:\s*(\[[^\]]+\])[^{}]*\}',
        block,
        re.DOTALL,
    )
    if not series_blocks:
        # Simpler pattern: just data arrays in order
        data_matches = re.findall(r'\bdata\s*:\s*(\[[^\]]+\])', block)
        name_matches = re.findall(r'\bname\s*:\s*["\']([^"\']+)["\']', block)
        for i, dm in enumerate(data_matches):
            nums = [float(n) for n in re.findall(r'-?[\d.]+', dm)]
            name = name_matches[i] if i < len(name_matches) else f"series_{i}"
            series.append({"name": name, "data": nums})
    else:
        for name, data_str in series_blocks:
            nums = [float(n) for n in re.findall(r'-?[\d.]+', data_str)]
            series.append({"name": name, "data": nums})

    return {"categories": categories, "series": series}


def to_int_list(lst):
    return [int(abs(x)) for x in lst]


# ── Dataset builders ───────────────────────────────────────────────────────────

def build_annual(html: str) -> pd.DataFrame:
    """Annual national totals 2018–2026."""
    chart = extract_chart(html, "year_case")
    years = [int(y) for y in chart["categories"] if y.isdigit()]
    cases = to_int_list(chart["series"][0]["data"]) if chart["series"] else []
    # Pad/trim to match
    n = min(len(years), len(cases))
    df = pd.DataFrame({"year": years[:n], "dengue_cases": cases[:n]})
    # Add deaths — from a separate chart if available
    death_chart = extract_chart(html, "death_case_in_year")
    LOG.append(f"Annual: {len(df)} year rows")
    return df


def build_monthly(html: str) -> pd.DataFrame:
    """Monthly national cases for embedded years (2023, 2024, 2025)."""
    chart = extract_chart(html, "by_month_case")
    months = chart["categories"]  # Jan–Dec
    rows = []
    for s in chart["series"]:
        # name like "Affected (Admitted) by Month in 2023"
        year_m = re.search(r"\b(20\d{2})\b", s["name"])
        if not year_m:
            continue
        year = int(year_m.group(1))
        data = to_int_list(s["data"])
        for i, val in enumerate(data):
            if i < len(months):
                rows.append({"year": year, "month": months[i], "month_num": i + 1, "dengue_cases": val})
    df = pd.DataFrame(rows).sort_values(["year", "month_num"])
    LOG.append(f"Monthly: {len(df)} rows across {df['year'].nunique() if not df.empty else 0} years")
    return df


def build_weekly(html: str) -> pd.DataFrame:
    """Weekly national cases for embedded years (2023, 2024, 2025)."""
    chart = extract_chart(html, "by_week_case")
    # categories are week labels W01–W52
    weeks_raw = chart["categories"]
    rows = []
    for s in chart["series"]:
        year_m = re.search(r"\b(20\d{2})\b", s["name"])
        if not year_m:
            continue
        year = int(year_m.group(1))
        data = to_int_list(s["data"])
        # Skip index 0 (blank category)
        start = 1 if weeks_raw and weeks_raw[0] in ("", " ", ",") else 0
        for i, val in enumerate(data[start:], start=start):
            week_label = weeks_raw[i] if i < len(weeks_raw) else f"W{i:02d}"
            week_num = i  # W01 = week 1
            rows.append({
                "year": year,
                "week": week_label.strip(",").strip() or f"W{i:02d}",
                "week_num": week_num,
                "dengue_cases": val,
            })
    df = pd.DataFrame(rows).sort_values(["year", "week_num"])
    LOG.append(f"Weekly: {len(df)} rows")
    return df


def build_daily_2026(html: str) -> pd.DataFrame:
    """Daily national cases Jan–present 2026."""
    chart = extract_chart(html, "confirmed_case")
    dates = chart["categories"]   # "01-Jan-26", "02-Jan-26", ...
    cases = to_int_list(chart["series"][0]["data"]) if chart["series"] else []
    n = min(len(dates), len(cases))
    rows = []
    for i in range(n):
        date_str = dates[i].translate(BANGLA_DIGITS).strip()
        try:
            dt = datetime.strptime(date_str, "%d-%b-%y")
            date_iso = dt.strftime("%Y-%m-%d")
        except ValueError:
            date_iso = date_str
        rows.append({"date": date_iso, "dengue_cases_daily": cases[i]})
    df = pd.DataFrame(rows)
    LOG.append(f"Daily 2026: {len(df)} days ({df['date'].min() if not df.empty else '?'} to {df['date'].max() if not df.empty else '?'})")
    return df


def build_division_2026(html: str) -> pd.DataFrame:
    """Division-level cumulative cases and deaths for 2026 (Jan–present)."""
    # Cases
    case_chart = extract_chart(html, "division_case")
    divs = case_chart["categories"]
    cases = to_int_list(case_chart["series"][0]["data"]) if case_chart["series"] else []

    # Deaths
    death_chart = extract_chart(html, "division_death")
    death_divs = death_chart["categories"]
    deaths = to_int_list(death_chart["series"][0]["data"]) if death_chart["series"] else []

    # Build case rows
    n = min(len(divs), len(cases))
    rows = []
    for i in range(n):
        div_name = divs[i].strip()
        # Skip city corporations in this table (keep only 8 divisions)
        if any(cc in div_name for cc in ["DSCC", "DNCC", "CC"]):
            continue
        rows.append({
            "year": 2026,
            "division": div_name,
            "dengue_cases_cumulative": cases[i],
            "dengue_deaths_cumulative": 0,
        })

    # Add deaths
    death_map = {}
    for i in range(min(len(death_divs), len(deaths))):
        dv = death_divs[i].strip()
        if not any(cc in dv for cc in ["DSCC", "DNCC", "CC"]):
            death_map[dv] = deaths[i]

    for row in rows:
        row["dengue_deaths_cumulative"] = death_map.get(row["division"], 0)

    df = pd.DataFrame(rows).sort_values("dengue_cases_cumulative", ascending=False)
    LOG.append(f"Division 2026: {len(df)} divisions")
    return df


def build_weekly_division_2026(html: str) -> pd.DataFrame:
    """Weekly cases by division for 2026."""
    chart = extract_chart(html, "affected_in_division_by_week")
    weeks = chart["categories"]  # W01–W22 etc.
    rows = []
    for s in chart["series"]:
        division = s["name"]
        data = to_int_list(s["data"])
        for i, val in enumerate(data):
            week = weeks[i] if i < len(weeks) else f"W{i+1:02d}"
            rows.append({
                "year": 2026,
                "week": week,
                "week_num": i + 1,
                "division": division,
                "dengue_cases": val,
            })
    df = pd.DataFrame(rows).sort_values(["division", "week_num"])
    LOG.append(f"Weekly division 2026: {len(df)} rows, {df['division'].nunique() if not df.empty else 0} divisions")
    return df


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("DGHS Bangladesh — Dengue Dashboard Scraper")
    print(f"Run date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    html = fetch_dashboard()

    print("\nExtracting datasets...")

    datasets = {
        "dengue_annual_national":      build_annual(html),
        "dengue_monthly_national":     build_monthly(html),
        "dengue_weekly_national":      build_weekly(html),
        "dengue_daily_2026":           build_daily_2026(html),
        "dengue_division_2026":        build_division_2026(html),
        "dengue_weekly_division_2026": build_weekly_division_2026(html),
    }

    print("\nSaving CSVs...")
    for name, df in datasets.items():
        path = OUT_DIR / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  {path.name}: {len(df)} rows")

    # Save log
    log_path = OUT_DIR / "dengue_scrape_log.txt"
    with open(log_path, "w") as f:
        f.write(f"Run: {datetime.now().isoformat()}\n\n")
        for entry in LOG:
            f.write(f"  {entry}\n")

    print(f"\nLog: {log_path}")

    # ── Previews ──
    print("\n── Annual National (2018–2026) ──")
    print(datasets["dengue_annual_national"].to_string(index=False))

    print("\n── Monthly (2023 Jan–Dec) ──")
    df23 = datasets["dengue_monthly_national"]
    if not df23.empty:
        print(df23[df23["year"] == 2023][["year","month","dengue_cases"]].to_string(index=False))

    print("\n── Division 2026 ──")
    print(datasets["dengue_division_2026"].to_string(index=False))


if __name__ == "__main__":
    main()
