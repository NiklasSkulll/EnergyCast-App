# Glossary and Term Explanations

This glossary explains key terms, methods, and metrics used in EnergyCast-App in plain language.
If a scientific source is needed, use a placeholder like [CITATION NEEDED].

## Power System and Energy Terms

**Electricity Load (Demand)**
The total power consumed by end users at a given time, typically measured in megawatts (MW). In this project it is the target variable for Germany.

**Renewable Generation**
Electricity produced from renewable sources such as wind and solar. These sources are weather-dependent and add volatility to the grid.

**Wind Generation (Onshore/Offshore)**
Power produced by wind turbines on land (onshore) or at sea (offshore). Offshore tends to be steadier but can have different seasonal patterns.

**Solar Generation**
Power produced by photovoltaic systems. It strongly depends on daylight and cloud cover and typically peaks at midday.

**ENTSO-E Transparency Platform**
European platform for electricity system data reporting. Many load and generation series are derived from this source. [CITATION NEEDED]

## Time Series Concepts

**Time Series**
Data recorded in chronological order, often at regular intervals. Here: hourly values.

**Seasonality**
Recurring patterns over time (daily, weekly, yearly) driven by human activity and weather.

**Lag Features**
Previous values of a time series used as predictors (e.g., load at t-1h, t-24h, t-168h).

**Rolling Mean**
Average computed over a moving window of past values (e.g., 24-hour rolling mean) to smooth short-term noise.

**Time-Aware Split**
Train/validation/test splits that preserve chronological order to avoid leakage from future data.

## Data Quality

**Missing Values**
Entries that are null or empty. High missingness can bias results or require imputation.

**Duplicates**
Repeated rows or timestamps. In time series, duplicate timestamps can indicate ingestion errors.

**Outliers**
Unusually large or small values. Outliers can represent real events or data errors and should be reviewed carefully.

## Machine Learning and Metrics

**Feature**
An input variable used by the model (e.g., temperature, hour of day, wind generation).

**Target Variable**
The variable the model predicts. Here: Germany's hourly load.

**MAE (Mean Absolute Error)**
Average absolute difference between predictions and actual values. Interpretable in MW.

**RMSE (Root Mean Squared Error)**
Square root of the mean squared error. Penalizes large errors more than MAE.

**sMAPE (Symmetric Mean Absolute Percentage Error)**
Scale-independent percentage error that penalizes over- and under-forecasting equally. [CITATION NEEDED]

**R2 (Coefficient of Determination)**
Measures the proportion of variance explained by the model. Values close to 1 indicate strong explanatory power.

**Overfitting**
When a model learns noise in the training data and performs poorly on new data.

**Data Leakage**
When information from the future or test set leaks into training, causing overly optimistic results.

## Process Model

**QUA3CK**
A structured ML process model: Question, Understanding, Algorithm selection/Adaptation/Adjustment, Conclude, Knowledge transfer.

**Phase Q (Question)**
Defines the problem, stakeholders, KPIs, scope, and evaluation design.

**Phase U (Understanding)**
Exploratory data analysis to assess structure, quality, distributions, and readiness for modeling.

**Phase A3**
Algorithm selection, feature engineering, and hyperparameter tuning.

**Phase C**
Compare models and decide on the final approach.

**Phase K**
Knowledge transfer, documentation, and delivery artifacts.

## DIG Framework

**Description**
Inspect columns, samples, and basic data structure.

**Introspection**
Formulate questions, identify limitations, and validate what the data can answer.

**Goal Setting**
Decide whether data is suitable and define next steps for modeling.
