# Smart Grid Load Forecasting for Sustainable Energy Planning

## Project Overview

This project investigates how weather conditions, renewable energy generation, calendar effects, and historical electricity demand can be used to forecast the hourly electricity load in Germany.

The project is part of a university course in **Data Analytics und Big Data** and follows the **QUA³CK process model**:

- **Q** – Question
- **U** – Understanding the Data
- **A³** – Algorithm Selection, Adapting Features, Adjusting Hyperparameters
- **C** – Conclude & Compare
- **K** – Knowledge Transfer

The main goal is to build a data-driven forecasting pipeline that predicts electricity demand and supports sustainable energy planning. Accurate load forecasting is important because it can help grid operators, energy analysts, and infrastructure planners integrate renewable energy more efficiently, reduce the need for fossil backup power, and improve the stability of smart grids.

## Research Question

**English:**
- _How accurately can Germany's hourly electricity load for the period 2015–2019 be forecasted using weather data, renewable electricity generation, calendar effects, and historical load data?_

**German:**
- _Wie gut lässt sich die stündliche Stromlast Deutschlands im Zeitraum 2015–2019 anhand von Wetterdaten, erneuerbarer Stromerzeugung, Kalendereffekten und historischen Lastwerten prognostizieren?_

## Sustainability Relevance

Electricity systems are becoming increasingly dependent on renewable energy sources such as wind and solar power. These sources are strongly influenced by weather conditions and are less predictable than conventional energy generation.

This project connects several sustainability-related aspects:

```text
weather and climate conditions
↓
renewable energy generation
↓
electricity demand patterns
↓
smart grid forecasting
↓
more efficient integration of renewable energy
````

By analyzing and predicting electricity demand, the project contributes to the broader goal of making energy systems more efficient, flexible, and sustainable.

## Target Variable

The main target variable is:

```text
hourly electricity load / demand in Germany
```

The model tries to predict the electricity demand for a specific hour using historical, weather-related, renewable-energy-related, and calendar-based features.

## Input Features

Possible input features include:

```text
temperature
solar radiation
wind generation
solar generation
electricity price
hour of day
weekday
weekend indicator
month
season
previous hour electricity demand
previous day same-hour electricity demand
previous week same-hour electricity demand
rolling demand averages
```

## Data Sources

The project uses public energy and weather datasets, especially from **Open Power System Data (OPSD)**.

Planned datasets:

1. **OPSD Time Series**

   * Hourly electricity load
   * Wind generation
   * Solar generation
   * Electricity prices
   * Country/zone-based time series

2. **OPSD Weather Data**

   * Temperature
   * Solar radiation
   * Wind-related weather variables
   * Hourly weather data for European countries

The datasets can be joined using timestamps and country or zone information, with a focus on Germany.

## Methodology

The project follows the QUA³CK process model.

### Q — Question

In this phase, the research question, target group, project goal, and success metrics are defined.

The main research question is:

> Wie gut lässt sich die stündliche Stromlast Deutschlands im Zeitraum 2015–2019 anhand von Wetterdaten, erneuerbarer Stromerzeugung, Kalendereffekten und historischen Lastwerten prognostizieren?

Target groups:

```text
grid operators
energy analysts
public infrastructure planners
students and researchers in energy analytics
```

Success metrics:

```text
MAE
RMSE
sMAPE
R²
```

### U — Understanding the Data

In this phase, the datasets are explored and analyzed.

Main questions:

```text
When is electricity demand highest?
How does electricity demand change by hour, weekday, month, and season?
Does demand increase during winter or summer?
Does temperature correlate with electricity demand?
Does solar radiation correlate with solar generation?
How do wind and solar generation behave over time?
Are weekdays different from weekends?
Are there missing values or outliers?
Are there seasonal patterns in load and renewable generation?
```

Planned analyses:

```text
missing value analysis
descriptive statistics
time-series plots
seasonal demand patterns
correlation analysis
weekday/weekend comparison
load vs. temperature analysis
renewable generation vs. weather analysis
```

### A³ — Algorithms, Features, Hyperparameters

In this phase, different forecasting models are trained, feature sets are adapted, and model parameters are optimized.

Possible models:

```text
naive baseline model
linear regression
ridge regression
random forest regression
gradient boosting regression
XGBoost or LightGBM
```

Possible feature groups:

```text
calendar features
weather features
renewable generation features
historical load features
lag features
rolling mean features
```

Example lag features:

```text
load_lag_1h
load_lag_24h
load_lag_168h
rolling_mean_24h
rolling_mean_168h
```

The models will be compared using time-aware train, validation, and test splits instead of random splitting.

Example split:

```text
training data: 2015–2017
validation data: 2018
test data: 2019
```

### C — Conclude & Compare

In this phase, the trained models are compared quantitatively and qualitatively.

Main comparison questions:

```text
Which model performs best?
Does adding weather data improve the prediction?
Does adding renewable generation improve the prediction?
Do lag features improve the prediction?
Are prediction errors higher in winter or summer?
Are peak-load hours harder to predict?
Is the best model also interpretable and practical?
```

Planned evaluation metrics:

```text
MAE
RMSE
sMAPE
R²
prediction error by season
prediction error by hour of day
prediction error during peak-load periods
```

The comparison should show whether weather, renewable generation, and historical demand values provide measurable value for electricity load forecasting.

### K — Knowledge Transfer

In this phase, the results are documented and prepared for presentation.

Planned project outputs:

```text
GitHub repository
Jupyter notebooks for the QUA³CK phases
cleaned and processed datasets
model comparison tables
visualizations
final report
README documentation
optional Streamlit dashboard or web app
```

Possible dashboard features:

```text
show historical electricity load
show renewable generation patterns
visualize predicted vs. actual demand
display model performance metrics
allow simple exploration by date or season
```

## Expected Outcome

The expected result is a reproducible data analytics and machine learning project that shows how well hourly electricity demand in Germany can be predicted using a combination of:

```text
weather data
renewable energy generation
calendar effects
historical electricity load
```

The project should demonstrate the full QUA³CK process from problem definition to knowledge transfer and provide insights into how data analytics can support sustainable energy systems and smart grid planning.
