# AI Prompt for Phase Q

## Initial prompt for data base research

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

```markdown
"**Energie und Smart Grid** ist für diese Aufgabe die stärkste Richtung. Der Grund ist nicht nur die fachliche Relevanz von Nachhaltigkeit, Klima und Infrastruktur, sondern vor allem die Datenlogik: Stromlast, Preise, Wind- und Solarerzeugung liegen als Zeitreihen vor; Wetterdaten liefern unmittelbar passende exogene Variablen; und die Daten lassen sich über **Stunde** und **Land/Zone** sauber verknüpfen. Das offizielle OPSD-Zeitreihenpaket deckt stündliche Last-, Preis- sowie Wind- und Solardaten für 32 europäische Länder bzw. Zonen ab; das zugehörige Wetterpaket liefert stündliche Temperatur- und Strahlungsdaten für europäische Länder."

Can you give me the links to these data bases
```

## Prompt for concept the phase Q

```markdown
I need to do the phase Q of my project and write it into this file notebooks/01_Q_Phase.ipynb in markdown.
Gather all information you need to finish phase Q and write phase Q in bulletpoints.
```