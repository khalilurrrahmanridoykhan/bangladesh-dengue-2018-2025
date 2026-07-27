.PHONY: data reproduce manuscript

data:
	python scrape_dengue_dashboard.py

reproduce:
	python analysis/01_annual_trend.py
	python analysis/02_epidemic_curve.py
	python analysis/03_seasonal_pattern.py
	python analysis/04_division_analysis.py
	python analysis/05_summary_stats.py

manuscript:
	python write_manuscript.py
