# AI Prompt for Phase Q

## Initial prompt for data base research

**ChatGPT 5.5 Thinking ([AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md)):**
```markdown
# Role
You are an expert data analytics and big data project advisor with strong experience in public datasets, machine learning project design, and the QUA³CK process model.

# Task
Help me identify suitable public datasets for a Data Analytics / Big Data project and develop a concrete research question that can be analyzed using the QUA³CK process model.

The project should preferably be related to one of these broad areas:

- sustainability
- climate / environment
- energy
- mobility
- IT networks / cybersecurity
- smart cities
- public infrastructure
- economy and society

I do not yet have a final topic. Your task is to help me find a strong topic by comparing multiple possible dataset combinations.

# Context
This is for a university project in the course “Data Analytics und Big Data”.

The project must follow the QUA³CK process model:

| Phase | Meaning | Goal |
|---|---|---|
| Q | Question | Define a clear research question, target group, objective, and success metrics |
| U | Understanding the Data | Analyze data structure, quality, missing values, distributions, correlations, and patterns |
| A³ | Algorithm Selection, Adapting Features, Adjusting Hyperparameters | Select algorithms, engineer features, train models, and optimize hyperparameters |
| C | Conclude & Compare | Compare models using quantitative and qualitative criteria |
| K | Knowledge Transfer | Document results and make them usable through notebooks, README, GitHub repo, report, or simple app |

The assignment says:

> Search for multiple high-volume datasets from Kaggle or similar sources that correlate with each other and design notebooks for the individual QUA³CK phases based on a research question you develop.

The final project should include:

- several public datasets that can be meaningfully combined or compared
- one clear research question
- a GitHub repository structure
- Jupyter notebooks for the QUA³CK phases
- a README outline
- possible use of tools like GitHub Copilot, Claude Code, or Codex
- inspiration from projects like: https://github.com/noahrsn/Degrees-of-No-Return-App

# Public Dataset Sources
Search and recommend datasets from these sources:

- Kaggle Datasets: https://www.kaggle.com/datasets
- UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/index.php
- Google Dataset Search: https://datasetsearch.research.google.com
- AWS Open Data Registry: https://registry.opendata.aws
- OpenML: https://www.openml.org
- Data.gov: https://www.data.gov
- European Data Portal: https://data.europa.eu

# Requirements for Dataset Recommendations
For each suggested dataset or dataset combination, evaluate:

1. Source and link
2. Topic area
3. Dataset size / volume
4. Available columns or feature types
5. Target variable, if available
6. Whether it supports supervised learning, unsupervised learning, time-series analysis, or exploratory analysis
7. How it could be connected with another dataset
8. Possible research question
9. Suitability for the QUA³CK process
10. Difficulty level for a student project
11. Possible risks, such as missing data, unclear licenses, too much preprocessing, or weak correlation

# Preferred Output
Please produce the answer in this structure:

## 1. Short Project Direction Recommendation
Briefly recommend 2–3 promising topic directions and explain which one is best for this assignment.

## 2. Dataset Candidate Table
Create a table with at least 6 dataset candidates.

Columns:

- Dataset name
- Source
- Topic
- Link
- Data volume
- Main variables
- Possible analysis
- Suitability score from 1–10

## 3. Best Dataset Combination
Choose the best combination of 2–4 datasets that could plausibly correlate with each other.

Explain:

- why these datasets belong together
- what can be analyzed
- which variables may correlate
- what the expected analytical value is

## 4. Final Research Question
Create one strong research question in German.

The research question should be specific, measurable, and suitable for data analytics or machine learning.

Also provide 2–3 alternative research questions.
```

## Prompt for data base sources

**ChatGPT 5.5 Thinking [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
"**Energie und Smart Grid** ist für diese Aufgabe die stärkste Richtung. Der Grund ist nicht nur die fachliche Relevanz von Nachhaltigkeit, Klima und Infrastruktur, sondern vor allem die Datenlogik: Stromlast, Preise, Wind- und Solarerzeugung liegen als Zeitreihen vor; Wetterdaten liefern unmittelbar passende exogene Variablen; und die Daten lassen sich über **Stunde** und **Land/Zone** sauber verknüpfen. Das offizielle OPSD-Zeitreihenpaket deckt stündliche Last-, Preis- sowie Wind- und Solardaten für 32 europäische Länder bzw. Zonen ab; das zugehörige Wetterpaket liefert stündliche Temperatur- und Strahlungsdaten für europäische Länder."

Can you give me the links to these data bases
```

## Prompt for concept the phase Q

**GPT-5.2-Codex [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
I need to do the phase Q of my project and write it into this file notebooks/01_Q_Phase.ipynb in markdown.
Gather all information you need to finish phase Q and write phase Q in bulletpoints.
```

## Prompt for finishing the phase Q

**Claude Sonnet 4.6 [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
You are an expert data science mentor specializing in Data Analytics, Big Data, machine learning, and academic project documentation.

I am working on a university project in the course "Data Analytics and Big Data." The project follows the QUA³CK process model (Stock, S., Becker, J., Grimm, D., Hotfilter, T., Molinar, G., Stang, M., & Stork, W. (2021). QUA³CK – A Machine Learning Development Process. KIT.), especially the Q phase, where the research question, target group, KPIs, success metrics, deployment goal, and project scope must be clearly defined.

---

## Project Context

Project topic: Smart Grid Load Forecasting for Sustainable Energy Planning

Goal: Forecast Germany's hourly electricity load using weather data, renewable electricity generation, calendar effects, historical electricity load data, and machine learning algorithms.

The project is written in Jupyter Notebooks and follows the QUA³CK phases:
- Q — Question
- U — Understanding the Data
- A³ — Algorithm Selection, Adapting Features, Adjusting Hyperparameters
- C — Conclude & Compare
- K — Knowledge Transfer

---

## Research Question

"To what extent can machine learning regression models forecast Germany's hourly electricity load for the period 2015–2019, using weather data, renewable electricity generation, calendar effects, and historical lag features, achieving a symmetric mean absolute percentage error (sMAPE) of 5 % or below on a time-aware held-out test set (2019)?"

German version:
"Inwieweit können Machine-Learning-Regressionsmodelle die stündliche Stromlast Deutschlands im Zeitraum 2015–2019 auf Basis von Wetterdaten, erneuerbarer Stromerzeugung, Kalendereffekten und historischen Lag-Features mit einem symmetrischen mittleren absoluten prozentualen Fehler (sMAPE) von maximal 5 % auf einem zeitlich getrennten Testdatensatz (2019) prognostizieren?"

---

## Fixed Project Decisions

These are already decided and must not be changed:

1. Evaluation design — time-aware split, no random splitting:
   - Training   : 2015–2017
   - Validation : 2018
   - Test        : 2019 (held out, used exactly once)

2. Primary KPI: sMAPE (Symmetric Mean Absolute Percentage Error)
   - Single primary KPI only — gives a clear, unambiguous go/no-go answer
   - Success criterion: sMAPE ≤ 5 % (≥ 95 % forecasting accuracy) on the 2019 test set
   - Supporting metrics (reported but not primary): RMSE, MAE, R²

3. Target variable:
   - Variable: DE_load_actual_entsoe_transparency
   - Source: Open Power System Data (OPSD) Time Series
   - Unit: Megawatts (MW), hourly UTC timestamps
   - Coverage: Germany, 2015-01-01 00:00 to 2019-12-31 23:00

4. Three hypotheses:
   - H1: Calendar and seasonal effects — a calendar-only model significantly outperforms the 24-hour naive persistence baseline on the 2019 test set.
   - H2: Weather and renewable generation — adding weather and renewable features to a calendar-only model reduces sMAPE by at least 10 % relative.
   - H3: Lag features — historical load lag features (t−1h, t−24h, t−168h) produce the largest individual RMSE reduction of any feature group added in isolation.

5. Input feature groups:
   - Calendar: hour_of_day, day_of_week, is_weekend, month, season, is_public_holiday
   - Weather: temperature_DE, solar_radiation_DE, wind_speed_DE
   - Renewable generation: wind_generation_DE, solar_generation_DE
   - Lag features: load_lag_1h, load_lag_24h, load_lag_168h, rolling_mean_24h, rolling_mean_168h

---

## Required Output

Produce a complete, ready-to-use Jupyter Notebook file for the Q phase in valid .ipynb JSON format.

The notebook must contain exactly these sections as markdown cells:

1. Title cell — "❓ Q Phase — Question" with QUA³CK phase indicator and Stock et al. (2021) citation
2. Problem Statement — 3 paragraphs connecting grid stability, Germany's renewable share (~35 % in 2019), forecasting need, and project description. Cite Bundesnetzagentur & Bundeskartellamt (2020) and ENTSO-E (2023).
3. Sustainability Relevance — bullet points on reduced fossil backup, better renewable integration, lower balancing costs, smart grid planning. Include the sustainability chain diagram as a code block. Cite IEA (2022).
4. Research Question — English and German versions in blockquote format.
5. Hypotheses — H1, H2, H3 each with hypothesis statement and test design. Cite Hong & Fan (2016) for H2, Hyndman & Athanasopoulos (2021) for H3.
6. Target Variable — formatted table with variable name, source, unit, resolution, coverage, period, task type. Cite Open Power System Data (2020).
7. Input Features — four subsections (Calendar, Weather, Renewable Generation, Lag Features), each as a formatted table with rationale. Cite Valor et al. (2001) for weather, Hyndman & Athanasopoulos (2021) for lag features.
8. Target Group and Stakeholders — table with three stakeholder groups and their value proposition.
9. Success Metric and Evaluation Design — three subsections:
   - 9.1 Primary KPI (sMAPE) with LaTeX formula, justification for why sMAPE is the single primary KPI, and the success criterion stated explicitly
   - 9.2 Supporting metrics table (RMSE, MAE, R²) with their subordinate roles
   - 9.3 Evaluation design table (Training/Validation/Test split) with explanation of why random splits must not be used. Cite Bergmeir & Benítez (2012).
10. Scope and Constraints — table of scope dimensions, exclusions list, assumptions list.
11. Deployment Goal and Deliverables — deployment goal statement and deliverables table (notebooks, processed datasets, model results, visualisations, README, optional Streamlit app).
12. References — all 9 citations in APA format:
    - Bergmeir & Benítez (2012)
    - Bundesnetzagentur & Bundeskartellamt (2020)
    - ENTSO-E (2023)
    - Hong & Fan (2016)
    - Hyndman & Athanasopoulos (2021)
    - IEA (2022)
    - Open Power System Data (2020)
    - Stock et al. (2021)
    - Valor et al. (2001)

---

## Format Requirements

- Output must be valid .ipynb JSON (nbformat 4, nbformat_minor 5)
- All content in markdown cells only — no code cells
- Use markdown tables, blockquotes, LaTeX for the sMAPE formula, and code blocks where specified
- Do not truncate or summarise any section — write the full content of every cell
- The file must be named 01_Q_Phase.ipynb
```