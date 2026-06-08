# bangladesh-dengue-2018-2025

**Epidemiological Characterisation of the Record 2023 Dengue Epidemic in Bangladesh: An 8-Year National Surveillance Analysis (2018–2025)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data: DGHS Bangladesh](https://img.shields.io/badge/Data-DGHS%20Bangladesh-blue)](https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php)
[![preprint: medRxiv](https://img.shields.io/badge/Preprint-medRxiv-red)](https://www.medrxiv.org)

---

## Authors

**Khalilur Rahman Ridoy Khan** *(Corresponding Author)*  
Independent Researcher, Dhaka, Bangladesh  
📧 khalilurrahmanridoykhan@gmail.com  
🐙 [@khalilurrrahmanridoykhan](https://github.com/khalilurrrahmanridoykhan)

**Watan Rahman**  
Institute of Science and Technology, Dhaka, Bangladesh

---

## Overview

This repository contains all data, analysis scripts, figures, and the manuscript for a study characterising the 2023 record dengue epidemic in Bangladesh using 8 years of national hospital surveillance data (2018–2025).

### Key Findings

| Metric | Value |
|--------|-------|
| 2023 admitted cases (record) | **321,017** |
| National incidence 2023 | **189.6 per 100,000** |
| Fold increase from 2018 baseline | **31.6×** |
| COVID-19 lockdown case reduction (2020) | **97.5%** |
| Monsoon burden (Jun–Oct, 2023) | **83.2% of annual cases** |
| Peak week 2023 | **W38 — 20,244 cases** |
| Post-2023 new baseline (2024–2025) | **~102,000/year** |
| Highest per-capita division | **Barishal (10.01/100,000)** |

---

## Data Source

All data were extracted from the **DGHS HEOC Dengue Dynamic Dashboard**:  
🔗 https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php

This is a publicly accessible government dashboard maintained by the Directorate General of Health Services (DGHS), Government of Bangladesh. No login or authentication is required. Data accessed: June 2026.

**Data represents admitted (hospitalised) dengue cases** — not total community infections.

---

## Repository Structure

```
bangladesh-dengue-2018-2025/
│
├── data/
│   └── raw/
│       ├── dengue_annual_national.csv        # Annual cases 2018–2026
│       ├── dengue_monthly_national.csv       # Monthly cases 2023–2025
│       ├── dengue_weekly_national.csv        # Weekly cases 2023–2025
│       ├── dengue_daily_2026.csv             # Daily cases Jan–Jun 2026
│       ├── dengue_division_2026.csv          # Division cases + deaths 2026 YTD
│       ├── dengue_weekly_division_2026.csv   # Weekly by division 2026
│       └── dengue_scrape_log.txt             # Scrape log
│
├── analysis/
│   ├── 01_annual_trend.py                    # Fig 1: Annual trend bar chart
│   ├── 02_epidemic_curve.py                  # Fig 2: Weekly epidemic curves
│   ├── 03_seasonal_pattern.py                # Fig 3: Monthly heatmap + seasonal index
│   ├── 04_division_analysis.py               # Fig 4: Division incidence + weekly trends
│   └── 05_summary_stats.py                   # Table 5: Key stats for manuscript
│
├── figures/
│   ├── fig1_annual_trend.png
│   ├── fig2_epidemic_curve.png
│   ├── fig3_seasonal_pattern.png
│   ├── fig4_division_analysis.png
│   ├── table1_annual_summary.csv
│   ├── table2_weekly_peaks.csv
│   ├── table3_seasonal_index.csv
│   ├── table4_division_incidence.csv
│   └── table5_key_stats.csv
│
├── scrape_dengue_dashboard.py                # Data collection script
├── write_manuscript.py                       # Generates Word manuscript
├── Bangladesh_Dengue_Manuscript.docx         # Full manuscript (Word)
├── README.md
└── LICENSE
```

---

## How to Reproduce

### 1. Install dependencies
```bash
pip install requests beautifulsoup4 pandas matplotlib seaborn scipy python-docx
```

### 2. Collect data from DGHS dashboard
```bash
python scrape_dengue_dashboard.py
```
Saves 6 CSV files to `data/raw/`.

### 3. Run analysis scripts in order
```bash
cd analysis
python 01_annual_trend.py
python 02_epidemic_curve.py
python 03_seasonal_pattern.py
python 04_division_analysis.py
python 05_summary_stats.py
```
Saves figures and tables to `figures/`.

### 4. Generate Word manuscript
```bash
python write_manuscript.py
```
Saves `Bangladesh_Dengue_Manuscript.docx`.

---

## Data Description

### `dengue_annual_national.csv`
| Column | Description |
|--------|-------------|
| year | Calendar year (2018–2026) |
| dengue_cases | Annual admitted dengue cases |

### `dengue_monthly_national.csv`
| Column | Description |
|--------|-------------|
| year | Calendar year |
| month | Month name |
| month_num | Month number (1–12) |
| dengue_cases | Monthly admitted dengue cases |

### `dengue_division_2026.csv`
| Column | Description |
|--------|-------------|
| year | 2026 |
| division | Administrative division name |
| dengue_cases_cumulative | Cumulative admitted cases (Jan–Jun 2026) |
| dengue_deaths_cumulative | Cumulative deaths (Jan–Jun 2026) |

---

## Citation

If you use this data or code, please cite:

> Khan KRR, Rahman W. Epidemiological Characterisation of the Record 2023 Dengue Epidemic in Bangladesh: An 8-Year National Surveillance Analysis (2018–2025). *medRxiv* [Preprint]. 2026. doi: [to be added after submission]

**Data source citation:**
> DGHS Bangladesh. HEOC Dengue Dynamic Dashboard. Directorate General of Health Services, Government of Bangladesh. Available at: https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php. Accessed June 2026.

---

## Ethics

This study used publicly available, aggregated surveillance data published by DGHS Bangladesh. No individual patient data were accessed. IRB review was not required.

---

## License

This repository is licensed under the [MIT License](LICENSE). Data originally sourced from DGHS Bangladesh (public government data).
