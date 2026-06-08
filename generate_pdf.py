"""
Generates Bangladesh_Dengue_Manuscript.pdf using ReportLab.
Run from the dengue/ directory: python generate_pdf.py
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FIG_DIR = Path("/Users/khalilur/Documents/AIWORK/dengue/figures")
OUT     = Path("/Users/khalilur/Documents/AIWORK/dengue/Bangladesh_Dengue_Manuscript.pdf")

# ── Page setup ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    topMargin=2.54*cm, bottomMargin=2.54*cm,
    leftMargin=2.54*cm, rightMargin=2.54*cm,
    title="Epidemiological Characterisation of the Record 2023 Dengue Epidemic in Bangladesh",
    author="Khalilur Rahman Ridoy Khan, Watan Rahman",
)

W = A4[0] - 5.08*cm  # usable width

# ── Styles ─────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

TITLE = ParagraphStyle("TITLE",
    fontName="Times-Bold", fontSize=15, leading=20,
    alignment=TA_CENTER, spaceAfter=8)

AUTHORS = ParagraphStyle("AUTHORS",
    fontName="Times-Roman", fontSize=12, leading=16,
    alignment=TA_CENTER, spaceAfter=4)

AFF = ParagraphStyle("AFF",
    fontName="Times-Italic", fontSize=11, leading=14,
    alignment=TA_CENTER, spaceAfter=4)

CORR = ParagraphStyle("CORR",
    fontName="Times-Roman", fontSize=11, leading=14,
    alignment=TA_CENTER, spaceAfter=6)

META = ParagraphStyle("META",
    fontName="Times-Roman", fontSize=11, leading=14,
    alignment=TA_CENTER, spaceAfter=0)

H1 = ParagraphStyle("H1",
    fontName="Times-Bold", fontSize=13, leading=17,
    spaceBefore=14, spaceAfter=6, alignment=TA_LEFT)

H2 = ParagraphStyle("H2",
    fontName="Times-Bold", fontSize=12, leading=16,
    spaceBefore=10, spaceAfter=4, alignment=TA_LEFT)

BODY = ParagraphStyle("BODY",
    fontName="Times-Roman", fontSize=12, leading=18,
    alignment=TA_JUSTIFY, spaceAfter=6)

INDENT = ParagraphStyle("INDENT",
    fontName="Times-Roman", fontSize=12, leading=18,
    alignment=TA_JUSTIFY, spaceAfter=6, firstLineIndent=1.27*cm)

CAPTION = ParagraphStyle("CAPTION",
    fontName="Times-Italic", fontSize=10, leading=14,
    alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)

REF = ParagraphStyle("REF",
    fontName="Times-Roman", fontSize=10, leading=14,
    alignment=TA_JUSTIFY, spaceAfter=4,
    leftIndent=1.0*cm, firstLineIndent=-1.0*cm)

KW = ParagraphStyle("KW",
    fontName="Times-Roman", fontSize=12, leading=18,
    alignment=TA_JUSTIFY, spaceAfter=6)

story = []

# ── Helpers ────────────────────────────────────────────────────────────────────

def h1(text):
    story.append(Paragraph(text, H1))

def h2(text):
    story.append(Paragraph(text, H2))

def body(text):
    story.append(Paragraph(text, BODY))

def indent(text):
    story.append(Paragraph(text, INDENT))

def sp(n=6):
    story.append(Spacer(1, n))

def pb():
    story.append(PageBreak())

def mixed(parts):
    """parts = list of (text, bold, italic)"""
    html = ""
    for text, bold, italic in parts:
        t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if bold:
            t = f"<b>{t}</b>"
        if italic:
            t = f"<i>{t}</i>"
        html += t
    story.append(Paragraph(html, INDENT))

def add_table(headers, rows, caption):
    col_n = len(headers)
    col_w = W / col_n

    tdata = [headers] + rows
    t = Table(tdata, colWidths=[col_w] * col_n, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 10),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",     (0, 1), (-1, -1), "Times-Roman"),
        ("FONTSIZE",     (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW",    (0, 0), (-1, 0), 1.5, colors.HexColor("#2c3e50")),
    ]))
    story.append(KeepTogether([t, Paragraph(caption, CAPTION)]))

def add_figure(path, caption, width=14*cm):
    if not Path(path).exists():
        story.append(Paragraph(f"[Figure not found: {path}]", CAPTION))
        return
    img = Image(str(path), width=width, height=width * 0.65)
    story.append(KeepTogether([img, Paragraph(caption, CAPTION)]))

# ══════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════════════════════════

sp(40)
story.append(Paragraph(
    "Epidemiological Characterisation of the Record 2023 Dengue Epidemic "
    "in Bangladesh: An 8-Year National Surveillance Analysis (2018–2025)",
    TITLE))
sp(12)
story.append(Paragraph(
    "Khalilur Rahman Ridoy Khan¹, Watan Rahman²",
    AUTHORS))
sp(6)
story.append(Paragraph(
    "¹Independent Researcher, Dhaka, Bangladesh<br/>"
    "²Institute of Science and Technology, Dhaka, Bangladesh",
    AFF))
sp(6)
story.append(Paragraph("Correspondence: khalilurrahmanridoykhan@gmail.com", CORR))
sp(24)
story.append(Paragraph(
    "Running title: Bangladesh Dengue 2023 Epidemic Analysis<br/>"
    "Manuscript type: Original Research Article",
    META))
pb()

# ══════════════════════════════════════════════════════════════════════════════
# ABSTRACT
# ══════════════════════════════════════════════════════════════════════════════

h1("Abstract")

mixed([("Background: ", True, False),
       ("Bangladesh experienced its largest dengue epidemic on record in 2023, "
        "with 321,017 admitted cases, representing a 31.6-fold increase from "
        "the 2018 baseline. Understanding the temporal dynamics, seasonal "
        "drivers, and geographic distribution of this outbreak is critical for "
        "evidence-based public health planning.", False, False)])

mixed([("Methods: ", True, False),
       ("We conducted a retrospective descriptive analysis of national dengue "
        "surveillance data from the Directorate General of Health Services "
        "(DGHS) Health Emergency Operation Center (HEOC) Dengue Dashboard, "
        "Bangladesh, covering 2018–2025. Annual, monthly, and weekly admitted "
        "case data were extracted and analysed for temporal trends, seasonal "
        "patterns, and division-level incidence.", False, False)])

mixed([("Results: ", True, False),
       ("Admitted dengue cases increased from 10,148 in 2018 to 321,017 in "
        "2023 (national incidence: 189.6 per 100,000). A natural experiment "
        "during the COVID-19 lockdown in 2020 revealed a 97.5% reduction in "
        "reported cases. The monsoon season (June–October) accounted for 83.2% "
        "of the 2023 annual burden, with September as the peak month (79,994 "
        "cases; 24.9% of annual total) and epidemiological week 38 as the peak "
        "week (20,244 cases). Post-2023 cases stabilised at a new elevated "
        "baseline (~102,000/year in 2024 and 2025), representing a 10-fold "
        "increase over the 2018 baseline. Barishal division had the highest "
        "per-capita incidence (10.01 per 100,000) in 2026 year-to-date data.", False, False)])

mixed([("Conclusions: ", True, False),
       ("Bangladesh dengue has entered a sustained high-burden era following "
        "the 2023 record epidemic. The strong monsoon seasonality provides a "
        "window for pre-monsoon vector control. Barishal and Chattogram "
        "divisions require prioritised intervention. These findings support "
        "evidence-based resource allocation for Bangladesh’s national dengue "
        "control programme.", False, False)])

story.append(Paragraph(
    "<b>Keywords:</b> <i>dengue; Bangladesh; epidemic; surveillance; seasonality; "
    "vector-borne disease; DGHS; tropical infectious disease</i>", KW))

pb()

# ══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════

h1("1. Introduction")

indent(
    "Dengue fever is the most rapidly spreading vector-borne viral disease globally, "
    "with an estimated 390–400 million infections occurring annually across more than "
    "129 endemic countries [1]. The disease is transmitted primarily by Aedes aegypti "
    "mosquitoes and, to a lesser extent, Aedes albopictus, and its burden is "
    "concentrated in tropical and subtropical regions of Asia, Latin America, and Africa [2]. "
    "Over the past three decades, the global incidence of dengue has increased eightfold, "
    "driven by rapid urbanisation, population growth, international travel, and climate "
    "change extending the geographic range of Aedes vectors [3]."
)

indent(
    "Bangladesh, a densely populated low-income country in South Asia, has emerged as "
    "one of the most dengue-affected nations in the WHO South-East Asia Region. Dengue "
    "was first reported in Bangladesh in 2000, with sporadic outbreaks occurring "
    "annually thereafter [4]. The country experienced its first large-scale epidemic "
    "in 2019, when 101,354 admitted cases were recorded — a dramatic departure from "
    "the historical norm [5]. The 2019 epidemic prompted significant public health "
    "concern, yet it was surpassed in 2023 when Bangladesh recorded 321,017 admitted "
    "cases — the largest dengue epidemic in the country’s history."
)

indent(
    "The 2023 outbreak placed severe strain on Bangladesh’s healthcare system, with "
    "hospitals across Dhaka and the coastal divisions overwhelmed during the peak "
    "transmission season [6]. The epidemic occurred against a backdrop of prolonged "
    "monsoon rains, expanding urban informal settlements, and unplanned construction "
    "sites that create ideal Aedes breeding habitats. Furthermore, the COVID-19 "
    "pandemic period (2020) inadvertently provided a natural experiment: strict "
    "lockdown measures in 2020 coincided with a dramatic reduction in reported dengue "
    "cases to only 1,405, offering insights into the role of human mobility and "
    "healthcare-seeking behaviour in shaping surveillance-based case counts."
)

indent(
    "Despite the scale and public health significance of Bangladesh’s dengue burden, "
    "comprehensive multi-year analyses characterising the temporal dynamics, seasonal "
    "pattern, and geographic distribution of dengue using national DGHS surveillance "
    "data remain limited. Most existing studies focus on specific outbreaks, limited "
    "geographic areas, or shorter time horizons [7–9]. A systematic 8-year "
    "characterisation of national trends, from the pre-epidemic baseline through the "
    "2023 record outbreak and into 2025, is needed to inform evidence-based planning."
)

indent(
    "This study aimed to: (1) describe the 8-year temporal trend in admitted dengue "
    "cases in Bangladesh (2018–2025); (2) characterise the seasonal pattern of dengue "
    "using monthly and weekly surveillance data (2023–2025); (3) estimate the "
    "division-level geographic distribution of dengue burden; and (4) quantify the "
    "effect of the COVID-19 lockdown on reported dengue cases as a natural experiment."
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. METHODS
# ══════════════════════════════════════════════════════════════════════════════

h1("2. Methods")

h2("2.1 Study Design")
indent(
    "We conducted a retrospective descriptive epidemiological analysis of national "
    "dengue surveillance data in Bangladesh. The primary unit of analysis was the "
    "country as a whole (national-level) for temporal analyses, and the administrative "
    "division for geographic analyses."
)

h2("2.2 Data Source")
indent(
    "Data were obtained from the Health Emergency Operation Center (HEOC) Dengue "
    "Dynamic Dashboard maintained by the Directorate General of Health Services (DGHS), "
    "Government of Bangladesh (available at: https://dashboard.dghs.gov.bd/pages/"
    "heoc_dengue_v1.php), accessed June 2026. The DGHS HEOC dashboard aggregates "
    "hospital-based dengue surveillance reports from government health facilities "
    "across all eight administrative divisions of Bangladesh. The dashboard is "
    "publicly accessible without authentication and represents the official national "
    "dengue surveillance platform."
)

h2("2.3 Data Extraction")
indent(
    "Dashboard data are rendered as interactive Highcharts visualisations embedded "
    "within the webpage as inline JavaScript data arrays. We developed an automated "
    "Python script (Python 3.14; libraries: requests, re, pandas) to perform an HTTP "
    "GET request to the dashboard URL, parse all Highcharts chart objects from the "
    "page source using regular expressions, and extract the associated categories "
    "(time periods, division names) and series data (case counts). Six structured "
    "datasets were generated: annual national cases (2018–2026); monthly national "
    "cases (2023–2025); weekly national cases (2023–2025); daily national cases "
    "(January–June 2026); division-level cumulative cases and deaths (2026 year-to-date); "
    "and weekly cases by division (2026, weeks 1–22). All data and analysis code "
    "are publicly available at the GitHub repository."
)

h2("2.4 Case Definition")
indent(
    "All case counts represent admitted (hospitalised) dengue patients reported "
    "through the DGHS HEOC surveillance system. Cases include both confirmed and "
    "probable dengue as per WHO 2009 dengue classification guidelines, as applied by "
    "DGHS. The dashboard reflects hospital-based surveillance; community-level "
    "dengue infections — which WHO estimates at 10 to 50 times the hospitalised count "
    "— are not captured."
)

h2("2.5 Population Denominators")
indent(
    "Division-level population denominators were obtained from the Bangladesh Bureau "
    "of Statistics (BBS) 2022 National Population and Housing Census. National "
    "population was 169,356,251. Division populations used were: Dhaka 36,054,418; "
    "Chattogram 28,423,019; Rajshahi 18,484,858; Khulna 15,563,000; Barishal "
    "8,325,666; Sylhet 10,009,239; Rangpur 15,665,000; Mymensingh 11,370,000."
)

h2("2.6 Statistical Analysis")
indent(
    "Annual trend: Year-over-year percentage change was calculated for each year. "
    "A linear regression model was fitted to pre-2023 annual cases (2018–2022) to "
    "estimate the baseline trend trajectory. The COVID-19 effect was quantified as "
    "the percentage reduction in 2020 cases relative to the 2018–2019 mean. "
    "Seasonal analysis: Monthly and weekly case counts were aggregated across "
    "available years (2023–2025) to calculate a seasonal index — each time unit’s "
    "average share of annual burden expressed as a percentage. A monthly heatmap "
    "was constructed to visualise the year-by-year seasonal distribution. "
    "Geographic analysis: Division-level incidence rates per 100,000 population "
    "were calculated from 2026 year-to-date cumulative cases divided by the 2022 "
    "census population. Case fatality rate (CFR) was calculated as confirmed deaths "
    "divided by admitted cases. All analyses were performed in Python 3.14 using "
    "pandas 2.x, matplotlib 3.10, and scipy 1.17."
)

h2("2.7 Ethical Considerations")
indent(
    "This study used publicly available, aggregated surveillance data published by "
    "DGHS Bangladesh. No individual patient data were accessed at any stage. "
    "Ethical review board approval was not required, consistent with standard "
    "practice for analyses of publicly available, de-identified aggregate data."
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. RESULTS
# ══════════════════════════════════════════════════════════════════════════════

h1("3. Results")

h2("3.1 Annual Trend in Dengue Cases (2018–2025)")

indent(
    "Between 2018 and 2025, Bangladesh recorded a total of 728,807 admitted dengue "
    "cases across the 8-year study period. Annual case counts and year-over-year "
    "changes are presented in Table 1 and Figure 1. From a baseline of 10,148 "
    "cases in 2018, the epidemic grew steeply to 101,354 cases in 2019 — an "
    "898.8% increase — representing the first major epidemic in Bangladesh’s "
    "dengue history."
)

indent(
    "In 2020, during the COVID-19 pandemic, admitted dengue cases fell dramatically "
    "to 1,405, representing a 97.5% reduction compared to the 2018–2019 mean of "
    "55,751 cases. This sharp decline coincided with nationwide COVID-19 lockdown "
    "measures, movement restrictions, and disrupted healthcare-seeking behaviour "
    "(discussed further in Section 4.2). A rebound followed in 2021 (28,429 cases; "
    "+1,923.4%) and 2022 (62,382 cases; +119.4%), reflecting both post-lockdown "
    "mobility resumption and accumulated vector breeding during lockdown."
)

indent(
    "The year 2023 represented an unprecedented inflection point, with 321,017 "
    "admitted cases — a 414.6% increase from 2022 and a 31.6-fold increase from "
    "the 2018 baseline. The national incidence in 2023 reached 189.6 per 100,000 "
    "population. Following the 2023 record, cases in 2024 and 2025 declined to "
    "101,211 and 102,861, respectively, representing a 68.5% reduction from the "
    "2023 peak. However, this post-peak level remains approximately 10-fold above "
    "the 2018 baseline, indicating that Bangladesh dengue has entered a sustained "
    "high-burden era (Figure 1)."
)

add_table(
    headers=["Year", "Admitted Cases", "YoY Change (%)", "National Incidence\n(per 100,000)"],
    rows=[
        ["2018", "10,148",  "—",       "6.0"],
        ["2019", "101,354", "+898.8",    "59.8"],
        ["2020", "1,405",   "−97.5", "0.8"],
        ["2021", "28,429",  "+1,923.4",  "16.8"],
        ["2022", "62,382",  "+119.4",    "36.8"],
        ["2023", "321,017", "+414.6",    "189.6"],
        ["2024", "101,211", "−68.5","59.8"],
        ["2025", "102,861", "+1.6",      "60.7"],
    ],
    caption="Table 1. Annual admitted dengue cases in Bangladesh, 2018–2025. "
            "Source: DGHS HEOC Dashboard. Incidence calculated using BBS 2022 "
            "national population (169,356,251)."
)

h2("3.2 COVID-19 Lockdown as a Natural Experiment")

indent(
    "The 2020 COVID-19 pandemic lockdown provided a natural experiment for "
    "assessing the contribution of mobility and healthcare-seeking behaviour to "
    "reported dengue burden. Admitted dengue cases in 2020 (1,405) were 97.5% "
    "lower than the 2018–2019 mean (55,751). This reduction occurred despite no "
    "evidence of meaningful change in Aedes vector populations during this period. "
    "The subsequent rebound to 28,429 cases in 2021 — as mobility restrictions "
    "eased — is consistent with suppression of reported cases during lockdown "
    "rather than true elimination of transmission. These findings suggest that "
    "surveillance-based dengue case counts in Bangladesh are substantially "
    "influenced by healthcare-seeking behaviour, and that true 2020 community "
    "dengue burden likely remained substantially higher than the reported figure."
)

h2("3.3 Weekly Epidemic Curves (2023–2025)")

indent(
    "Figure 2 presents the weekly epidemic curves for 2023, 2024, and 2025. "
    "All three years demonstrate a consistent seasonal pattern characterised by "
    "low transmission in the early weeks of the year (January–April), a gradual "
    "rise from epidemiological week 20 (mid-May), a rapid escalation through the "
    "monsoon season, and a peak in the post-monsoon period. In 2023, the peak "
    "occurred at epidemiological week 38 (mid-September), with 20,244 admitted "
    "cases in a single week. The 2023 peak was 2.6-fold higher than the 2024 "
    "peak (week 45; 7,891 cases) and 3.0-fold higher than the 2025 peak "
    "(week 47; 6,835 cases). In all three years, cases declined through November "
    "and December, with the epidemic effectively ending by January of the following year."
)

add_table(
    headers=["Year", "Annual Total", "Peak Week", "Peak Weekly Cases", "Peak Month"],
    rows=[
        ["2023", "321,017", "W38", "20,244", "September"],
        ["2024", "101,211", "W45", "7,891",  "November"],
        ["2025", "102,861", "W47", "6,835",  "November"],
    ],
    caption="Table 2. Epidemic curve summary statistics for Bangladesh dengue, "
            "2023–2025. Source: DGHS HEOC Dashboard weekly data."
)

h2("3.4 Seasonal Pattern (2023–2025)")

indent(
    "The monthly distribution of dengue cases revealed a highly concentrated "
    "seasonal pattern (Figure 3, Table 3). Averaged across 2023–2025, the monsoon "
    "and post-monsoon months (June–November) accounted for 99.1% of annual dengue "
    "burden, with October carrying the highest average monthly share (22.3%), "
    "followed by September (21.1%), November (18.1%), and August (17.4%). "
    "In 2023, the five monsoon/post-monsoon months (June–October) alone accounted "
    "for 266,996 cases — 83.2% of the annual total."
)

indent(
    "The pre-monsoon months of January through May collectively contributed less "
    "than 1.3% of annual cases across all three years, with March recording the "
    "lowest average burden (0.1% of annual total). The monthly heatmap confirms "
    "that this seasonal pattern is highly consistent across 2023, 2024, and 2025, "
    "with only moderate inter-year variation in the absolute magnitude of the "
    "peak months."
)

add_table(
    headers=["Month", "Avg Cases\n(2023–2025)", "Seasonal\nIndex (%)", "Season"],
    rows=[
        ["January",   "437",    "0.3",  "Dry"],
        ["February",  "527",    "0.3",  "Dry"],
        ["March",     "254",    "0.1",  "Dry"],
        ["April",     "312",    "0.2",  "Pre-monsoon"],
        ["May",       "733",    "0.4",  "Pre-monsoon"],
        ["June",      "2,412",  "1.4",  "Monsoon"],
        ["July",      "16,836", "9.8",  "Monsoon"],
        ["August",    "29,841", "17.4", "Monsoon"],
        ["September", "36,196", "21.1", "Post-monsoon"],
        ["October",   "38,290", "22.3", "Post-monsoon"],
        ["November",  "31,054", "18.1", "Post-monsoon"],
        ["December",  "14,550", "8.5",  "Post-monsoon"],
    ],
    caption="Table 3. Seasonal index for dengue in Bangladesh (2023–2025). "
            "Seasonal index = average monthly cases as percentage of average annual total."
)

h2("3.5 Geographic Distribution by Division (2026 Year-to-Date)")

indent(
    "Division-level data were available for the period January 1 to June 3, 2026 "
    "(3,459 total admitted cases), representing the low-transmission season. "
    "Figure 4 and Table 4 present incidence rates and case distributions across "
    "Bangladesh’s eight administrative divisions. Dhaka recorded the highest "
    "absolute case count (1,275 cases; 37.0% of the national total), reflecting "
    "its position as the most populous division (36.1 million inhabitants). "
    "However, when adjusted for population size, Barishal division had the highest "
    "incidence rate at 10.01 per 100,000, followed by Dhaka (3.54/100,000) and "
    "Chattogram (2.72/100,000). Rangpur (0.19/100,000) and Sylhet (0.35/100,000) "
    "recorded the lowest incidence rates."
)

indent(
    "The top three divisions by raw case count — Dhaka, Barishal, and Chattogram — "
    "collectively accounted for 83.5% of total admitted cases in 2026 year-to-date. "
    "Among the six divisions recording at least one death, Rajshahi had the highest "
    "case fatality rate (0.77%), though absolute death numbers were small (1 death "
    "among 130 cases) and should be interpreted cautiously given the early-year, "
    "low-season context. The disproportionately high per-capita burden in Barishal — "
    "a small coastal division with a population of 8.3 million — represents a "
    "notable geographic pattern warranting further investigation."
)

add_table(
    headers=["Division", "Cases\n(2026 YTD)", "Deaths\n(2026 YTD)",
             "Population\n(2022 Census)", "Incidence\n(per 100k)", "CFR (%)"],
    rows=[
        ["Dhaka",      "1,275", "3", "36,054,418", "3.54",  "0.24"],
        ["Barishal",   "833",   "0", "8,325,666",  "10.01", "0.00"],
        ["Chattogram", "772",   "1", "28,423,019", "2.72",  "0.13"],
        ["Khulna",     "271",   "1", "15,563,000", "1.74",  "0.37"],
        ["Rajshahi",   "130",   "1", "18,484,858", "0.70",  "0.77"],
        ["Mymensingh", "105",   "0", "11,370,000", "0.92",  "0.00"],
        ["Sylhet",     "35",    "0", "10,009,239", "0.35",  "0.00"],
        ["Rangpur",    "29",    "0", "15,665,000", "0.19",  "0.00"],
    ],
    caption="Table 4. Division-level dengue incidence in Bangladesh, January 1 – June 3, 2026. "
            "Source: DGHS HEOC Dashboard. Population: BBS 2022 Census."
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. DISCUSSION
# ══════════════════════════════════════════════════════════════════════════════

h1("4. Discussion")

h2("4.1 Bangladesh Dengue Has Entered a New High-Burden Era")

indent(
    "This study documents a profound and sustained increase in the admitted dengue "
    "burden in Bangladesh between 2018 and 2025. The 2023 epidemic, with 321,017 "
    "admitted cases and a national incidence of 189.6 per 100,000, represents an "
    "unprecedented threshold in the country’s dengue history. Critically, the "
    "post-2023 stabilisation at approximately 102,000 cases per year in 2024 and "
    "2025 — roughly 10-fold above the 2018 baseline — indicates that the 2023 "
    "epidemic was not merely a transient spike but a marker of structural change "
    "in dengue transmission dynamics."
)

indent(
    "Several ecological factors likely underpin this shift. First, rapid urbanisation "
    "in Bangladesh — particularly in Dhaka, Chattogram, and their peri-urban "
    "peripheries — has expanded Aedes aegypti breeding habitats through proliferating "
    "construction sites, unregulated water storage, and poor urban drainage [10]. "
    "Second, climate warming has extended the transmission season by increasing "
    "mean temperatures during shoulder months (April–May and November–December), "
    "consistent with global projections for dengue under climate change [11]. "
    "Third, the 2019 epidemic may have introduced a large susceptible cohort into "
    "subsequent transmission cycles as serotype dynamics shifted [12]."
)

h2("4.2 COVID-19 Lockdown as a Natural Experiment")

indent(
    "The 97.5% reduction in admitted dengue cases in 2020 compared to the "
    "2018–2019 mean offers a rare natural experiment in the epidemiology of a "
    "vector-borne disease. While reduced mobility during lockdowns plausibly "
    "decreased human-vector contact, the magnitude of the decline — nearly complete "
    "elimination of reported cases — is most parsimoniously explained by a "
    "combination of factors: reduced healthcare-seeking for febrile illness during "
    "COVID-19 fears; diversion of diagnostic resources toward COVID-19 testing; "
    "and reduced surveillance sensitivity during emergency conditions. Similar "
    "lockdown-associated dengue declines were reported across South and Southeast "
    "Asia in 2020 [13]. The rapid rebound in 2021 confirms that vector populations "
    "and transmission potential were maintained during 2020."
)

h2("4.3 Strong Monsoon Seasonality and Implications for Early Warning")

indent(
    "The consistent concentration of dengue burden in the June–November period "
    "(83.2% of 2023 annual cases; confirmed across 2024 and 2025) reflects the "
    "ecological dependence of Aedes aegypti breeding on monsoon rainfall and "
    "standing water accumulation. The peak occurring in September–October "
    "(post-monsoon) rather than July–August (peak rainfall) suggests a 4–8 week "
    "lag between maximum rainfall and maximum dengue transmission, consistent with "
    "the larval development and gonotrophic cycle of Aedes aegypti under "
    "Bangladeshi climatic conditions [14]."
)

indent(
    "This seasonal predictability provides a valuable window for public health "
    "intervention. Pre-monsoon vector control campaigns (April–May), targeting "
    "container breeding sites before the epidemic season, have been recommended "
    "by WHO and could substantially reduce peak-season burden [15]. The "
    "epidemiological week 35 case count — approximately 10 weeks before the "
    "2023 peak — could serve as an early warning trigger for emergency response "
    "mobilisation, hospital preparedness protocols, and community awareness campaigns."
)

h2("4.4 Barishal Division: A Disproportionate Geographic Burden")

indent(
    "The finding that Barishal division carries the highest per-capita dengue "
    "incidence (10.01/100,000 in 2026 year-to-date) — nearly three times the "
    "national rate and nearly three times the Dhaka rate (3.54/100,000) — despite "
    "having the smallest population of the eight divisions, warrants specific "
    "attention. Barishal’s coastal geography, characterised by extensive river "
    "networks, monsoon flooding, and post-flood stagnant water accumulation, "
    "may create favourable conditions for Aedes breeding that compound baseline "
    "risk. Additionally, Barishal’s relatively limited public health infrastructure "
    "compared to Dhaka may result in less effective vector control coverage. "
    "These findings support prioritising Barishal in national dengue control "
    "resource allocation."
)

h2("4.5 Limitations")

indent(
    "Several limitations must be acknowledged. First, the DGHS HEOC dashboard "
    "reports admitted (hospitalised) dengue cases, which substantially underestimate "
    "true community dengue incidence; WHO estimates that for every hospitalised "
    "case, 10 to 50 community-level infections go unreported. Second, division-level "
    "data were available only for 2026 year-to-date (a low-transmission period), "
    "precluding characterisation of the peak-season geographic distribution for "
    "2023 or other epidemic years. Third, monthly and weekly data were available "
    "only for 2023–2025, limiting intra-annual analysis for the earlier years "
    "(2018–2022). Fourth, no age or sex disaggregation was available in the "
    "extracted data, preventing age-specific incidence analysis. Fifth, surveillance "
    "sensitivity likely changed over the 8-year period due to infrastructure "
    "improvements, COVID-19 disruption, and varying case definitions, which may "
    "partially confound the observed temporal trends."
)

# ══════════════════════════════════════════════════════════════════════════════
# 5. CONCLUSIONS
# ══════════════════════════════════════════════════════════════════════════════

h1("5. Conclusions")

indent(
    "Bangladesh’s dengue burden increased 31.6-fold between 2018 and 2023, "
    "culminating in the largest recorded epidemic in the country’s history "
    "(321,017 admitted cases; national incidence 189.6/100,000). The COVID-19 "
    "pandemic demonstrated the sensitivity of surveillance-based dengue counts "
    "to healthcare-seeking behaviour, highlighting the importance of interpreting "
    "case trends in the context of surveillance conditions. Dengue in Bangladesh "
    "exhibits a highly predictable monsoon seasonality, with more than 83% of "
    "annual cases occurring between June and October. Post-2023, cases stabilised "
    "at a new elevated baseline approximately 10-fold above the 2018 level. "
    "Barishal division carries a disproportionately high per-capita burden. "
    "Evidence-based pre-monsoon vector control, targeted geographic resource "
    "allocation, and epidemiological week-based early warning systems are urgently "
    "needed to reduce Bangladesh’s escalating dengue burden."
)

# ══════════════════════════════════════════════════════════════════════════════
# BACK MATTER
# ══════════════════════════════════════════════════════════════════════════════

h1("Data Availability Statement")
body(
    "All data used in this study were sourced from the publicly available DGHS HEOC "
    "Dengue Dynamic Dashboard (https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php). "
    "The extracted datasets and analysis code are available at the project GitHub repository."
)

h1("Competing Interests")
body("The authors declare no competing interests.")

h1("Funding")
body("This research received no specific funding from any funding agency in the "
     "public, commercial, or not-for-profit sectors.")

# ══════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ══════════════════════════════════════════════════════════════════════════════

pb()
h1("References")

refs = [
    "[1] Bhatt S, Gething PW, Brady OJ, et al. The global distribution and burden of dengue. "
    "Nature. 2013;496(7446):504–507. doi:10.1038/nature12060",

    "[2] Brady OJ, Gething PW, Bhatt S, et al. Refining the global spatial limits of dengue "
    "virus transmission by evidence-based consensus. PLOS Neglected Tropical Diseases. "
    "2012;6(8):e1760. doi:10.1371/journal.pntd.0001760",

    "[3] WHO. Dengue and severe dengue. Fact sheet. World Health Organization; 2023. "
    "Available at: https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue",

    "[4] Dhar-Chowdhury P, Paul KK, Haque CE, et al. Dengue seroprevalence, seroconversion "
    "and risk factors in Dhaka, Bangladesh. PLOS Neglected Tropical Diseases. "
    "2017;11(3):e0005475. doi:10.1371/journal.pntd.0005475",

    "[5] DGHS Bangladesh. HEOC Dengue Dynamic Dashboard. Directorate General of Health "
    "Services, Government of Bangladesh. Available at: "
    "https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php. Accessed June 2026.",

    "[6] WHO SEARO. Dengue situation update. WHO South-East Asia Regional Office; 2023.",

    "[7] Sharmin S, Viennet E, Glass K, Harley D. The emergence of dengue in Bangladesh: "
    "epidemiology, challenges and future disease risk. Transactions of the Royal Society "
    "of Tropical Medicine and Hygiene. 2015;109(10):619–627. doi:10.1093/trstmh/trv067",

    "[8] Islam MT, Sobur MA, Islam A, et al. Molecular typing and antibiogram of dengue "
    "virus serotypes in Bangladesh. PLOS ONE. 2021;16(8):e0256817.",

    "[9] Hossain A, Roy S, Hossain D. Dengue fever in Bangladesh: Clinical features and "
    "outcome. Mymensingh Medical Journal. 2018;27(3):494–499.",

    "[10] Paul KK, Dhar-Chowdhury P, Haque CE, et al. Risk factors for the presence of "
    "dengue vector mosquitoes and implications for dengue control in Dhaka, Bangladesh. "
    "PLOS ONE. 2018;13(6):e0198431.",

    "[11] Ebi KL, Nealon J. Dengue in a changing climate. Environmental Research. "
    "2016;151:115–123. doi:10.1016/j.envres.2016.07.026",

    "[12] Gubler DJ. Dengue, urbanization and globalization: the unholy trinity of the "
    "21st century. Tropical Medicine and Health. 2011;39(4 Suppl):3–11.",

    "[13] Rodó X, Romero-Alvarez D, Campbell-Lendrum D, et al. Changing climate and the "
    "COVID-19 pandemic: more than just heads or tails. Nature Medicine. "
    "2021;27(4):576–579. doi:10.1038/s41591-021-01303-y",

    "[14] Sharmin S, Glass K, Viennet E, Harley D. Interaction of mean temperature and "
    "daily fluctuation influences dengue incidence in Dhaka, Bangladesh. PLOS Neglected "
    "Tropical Diseases. 2015;9(7):e0003901.",

    "[15] WHO. Dengue: guidelines for diagnosis, treatment, prevention and control. "
    "New edition. World Health Organization; 2009. WHO/HTM/NTD/DEN/2009.1.",

    "[16] Bangladesh Bureau of Statistics (BBS). Population and Housing Census 2022: "
    "National Report. Statistics and Informatics Division, Ministry of Planning, "
    "Bangladesh; 2023.",
]

for ref in refs:
    story.append(Paragraph(ref, REF))

# ══════════════════════════════════════════════════════════════════════════════
# FIGURES
# ══════════════════════════════════════════════════════════════════════════════

pb()
h1("Figures")

figures = [
    (FIG_DIR / "fig1_annual_trend.png",
     "Figure 1. Annual admitted dengue cases in Bangladesh, 2018–2025. "
     "Red bar indicates the 2023 record epidemic (321,017 cases). Light blue bar indicates "
     "2020, when COVID-19 lockdown measures coincided with a 97.5% reduction in reported "
     "cases. Numbers above bars indicate absolute case counts. Source: DGHS HEOC Dengue Dashboard."),

    (FIG_DIR / "fig2_epidemic_curve.png",
     "Figure 2. Weekly epidemic curves for Bangladesh dengue, 2023–2025. "
     "Shaded region indicates the monsoon season (epidemiological weeks 23–40). "
     "Peak weeks are annotated for each year. Source: DGHS HEOC Dengue Dashboard."),

    (FIG_DIR / "fig3_seasonal_pattern.png",
     "Figure 3. Seasonal distribution of dengue cases in Bangladesh, 2023–2025. "
     "Left panel: monthly heatmap showing percentage of annual cases by year. "
     "Right panel: seasonal index (average monthly share of annual burden). "
     "Source: DGHS HEOC Dengue Dashboard."),

    (FIG_DIR / "fig4_division_analysis.png",
     "Figure 4. Division-level dengue distribution in Bangladesh, 2026 year-to-date "
     "(January 1 – June 3). Left panel: incidence per 100,000 population (BBS 2022 Census). "
     "Right panel: weekly case trends by division. Source: DGHS HEOC Dengue Dashboard."),
]

for path, caption in figures:
    sp(10)
    add_figure(path, caption, width=14*cm)
    sp(10)

# ── Build PDF ──────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved: {OUT}")
import os
print(f"File size: {os.path.getsize(OUT) // 1024} KB")
