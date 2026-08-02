# Glossary and Term Explanations

This glossary explains key terms, methods and metrics used in EnergyCast-App in plain language.

## Power System and Energy Terms

**Electricity Load (Demand)**
The total power consumed by end users at a given time, typically measured in megawatts (MW) (European Network of Transmission System Operators for Electricity, n.d.). In this project it is Germany's national hourly actual load and is represented by `DE_load_actual_entsoe_transparency`.

**Open Power System Data (OPSD)**
The curated data platform used as the project source for public time-series and weather datasets (Open Power System Data, n.d.).

**OPSD Time Series Dataset**
The raw hourly file `data/raw/time_series_60min_singleindex.csv`. It provides the target load column, ENTSO-E load forecast column, renewable generation variables, capacity fields, profile fields, and other European power-system time series (Bundesnetzagentur, n.d.; ENTSO-E, 2023; Open Power System Data, 2020a).

**OPSD Weather Data**
The raw weather file `data/raw/weather_data.csv`. In this project it provides Germany-level temperature and radiation variables used as candidate predictors (Global Modeling and Assimilation Office, n.d.; Open Power System Data, 2020b; Renewables.ninja, 2018).

**Renewable Generation**
Electricity produced from renewable sources such as wind and solar. In this project, German wind and solar generation are candidate predictors and future scenario inputs; same-hour actual values are leakage-sensitive unless they would be known at prediction time (Intergovernmental Panel on Climate Change, 2011).

**Wind Generation (Onshore/Offshore)**
Power produced by wind turbines on land (onshore) or at sea (offshore) (Intergovernmental Panel on Climate Change, 2011). The project data includes Germany total wind, onshore wind, and offshore wind variables, with the selected app model using lagged total wind generation.

**Solar Generation**
Power produced by photovoltaic systems (International Energy Agency, n.d.). The selected app model uses lagged `DE_solar_generation_actual` values as part of the full lagged feature set.

**Germany `DE` Columns**
Country-code columns for Germany (Bundesnetzagentur, n.d.; ENTSO-E, 2023; Open Power System Data, 2020a). The project scope uses Germany national `DE` columns; `DE_LU` bidding-zone columns and German control-area columns are not interchangeable without a documented modeling decision.

**Weather Variables**
Germany-level weather predictors from OPSD Weather Data, especially `DE_temperature`, `DE_radiation_direct_horizontal`, and `DE_radiation_diffuse_horizontal` (Global Modeling and Assimilation Office, n.d.; Open Power System Data, 2020b; Renewables.ninja, 2018).

**ENTSO-E Transparency Platform**
European platform for electricity system data reporting. OPSD notes it as an original source for many load, forecast, and generation series used by this project (ENTSO-E, 2023).

## Time Series Concepts

**Time Series**
Data recorded in chronological order, often at regular intervals. Here: hourly values (Hyndman & Athanasopoulos, 2021).

**`utc_timestamp`**
The primary join key used to align the OPSD time-series and weather datasets. UTC is preferred for joins because local time can repeat or skip hours during daylight-saving-time transitions (Python Software Foundation, n.d.).

**`cet_cest_timestamp` / Local Timestamp**
Central European local time used for calendar interpretation after timestamp checks. The reusable code stores this normalized value as `local_timestamp` (Python Software Foundation, n.d.).

**Seasonality**
Recurring patterns over time (daily, weekly, yearly) driven by human activity and weather (Hyndman & Athanasopoulos, 2021).

**Calendar Features**
Predictors derived from timestamps, such as hour, weekday, weekend flag, month, and season. The selected feature set uses cyclical hour, weekday, and month encodings plus `is_weekend` (Hyndman & Athanasopoulos, 2021).

**Lag Features**
Previous values of a time series used as predictors (e.g., load at t-1h, t-24h, t-168h) (Hyndman & Athanasopoulos, 2021).

**Recursive Load Lags**
Future scenario logic where earlier model predictions become later lag inputs when actual future load is unavailable (Hyndman & Athanasopoulos, 2021).

**Rolling Mean**
Average computed over a moving window of past values (e.g., 24-hour rolling mean) to smooth short-term noise (Hyndman & Athanasopoulos, 2021). In this project, rolling load features are shifted before rolling so the target hour is not used in its own predictors.

**Forecast Horizon**
The time gap between forecast creation and the timestamp being predicted (Hyndman & Athanasopoulos, 2021). The Q phase marks the exact operational horizon as still needing a decision, while the Streamlit app exposes future scenario windows such as 24 hours, 48 hours, 7 days, and 30 days.

**Time-Aware Split**
Train/validation/test splits that preserve chronological order to avoid leakage from future data (Hyndman & Athanasopoulos, 2021; scikit-learn developers, n.d.d). The Q, U, A3, and C notebooks reserve 2019 as the final holdout year; after model selection, the app pipeline refits the selected estimator on 2015-2018 before using it for 2019 checks and future scenario forecasts.

## Data Quality

**Missing Values**
Entries that are null or empty. High missingness can bias results or require imputation (Little & Rubin, 2019).

**Duplicates**
Repeated rows or timestamps. In time series, duplicate timestamps can indicate ingestion errors (Batini & Scannapieco, 2016).

**Outliers**
Unusually large or small values. Outliers can represent real events or data errors and should be reviewed carefully (National Institute of Standards and Technology, 2022).

**Timestamp Alignment**
The process of making sure load, renewable generation, and weather rows refer to the same hourly point in time before joining or creating features (Batini & Scannapieco, 2016).

**Feature Availability Boundary**
The rule that a predictor may only be used if it would be available at the selected forecast creation time. This boundary is central to judging whether same-hour actual weather or renewable-generation values would create leakage (Kaufman et al., 2012).

## Machine Learning and Metrics

**Supervised Time-Series Regression**
A forecasting setup where a model learns from historical feature rows and a continuous numeric target (scikit-learn developers, n.d.b). EnergyCast uses this setup to predict hourly German load in MW.

**Feature**
An input variable used by the model (e.g., temperature, hour of day, wind generation) (scikit-learn developers, n.d.b).

**Target Variable**
The variable the model predicts. Here: Germany's hourly actual load, `DE_load_actual_entsoe_transparency` (scikit-learn developers, n.d.b).

**Feature Set**
A named group of predictors used by a candidate model (scikit-learn developers, n.d.b). The selected project model uses the `full lagged feature set`.

**Full Lagged Feature Set**
The selected feature group containing calendar features, past load values, rolling load statistics, lagged Germany weather variables, and lagged Germany solar and wind generation.

**HistGradientBoostingRegressor**
The scikit-learn regression model class used for the selected EnergyCast model  (scikit-learn developers, n.d.a).

**Scenario Forecast**
A forecast for future timestamps based on generated inputs and user-selected assumptions (Hyndman & Athanasopoulos, 2021). The app's 2020-2030 outputs are scenario forecasts, not measured future truth.

**Historical Seasonal Profiles**
Historical patterns grouped by calendar context, such as month, weekday, and hour (Hyndman & Athanasopoulos, 2021). The app uses these profiles to generate future weather, renewable, and load seed inputs.

**Holdout Test Year**
A final chronological test period kept separate from model selection (Hyndman & Athanasopoulos, 2021). In this project, 2019 is the holdout test year.

**Naive Persistence Baseline**
A simple reference forecast that reuses a past observed load value as the prediction, such as the same hour one day earlier (`load_lag_24h`) or one week earlier (`load_lag_168h`) (Hyndman & Athanasopoulos, 2021).

**ENTSO-E Day-Ahead Forecast**
The `DE_load_forecast_entsoe_transparency` column (Open Power System Data, 2020a). The project treats it as an external reference forecast or carefully validated optional feature, not as the target.

**MAE (Mean Absolute Error)**
Average absolute difference between predictions and actual values. Interpretable in MW (Hyndman & Koehler, 2006).

**RMSE (Root Mean Squared Error)**
Square root of the mean squared error. Penalizes large errors more than MAE (Hyndman & Koehler, 2006; scikit-learn developers, n.d.c).

**sMAPE (Symmetric Mean Absolute Percentage Error)**
Scale-independent percentage error used as the primary project KPI (Hyndman & Koehler, 2006; Makridakis, 1993). In this project, `sMAPE <= 5%` on the 2019 holdout is the main acceptance threshold, but it should not be described as literal "95% accuracy".

**R2 / R² (Coefficient of Determination)**
Measures the proportion of variance explained by the model. Values close to 1 indicate strong explanatory power (scikit-learn developers, n.d.c).

**Overfitting**
When a model learns noise in the training data and performs poorly on new data (scikit-learn developers, n.d.e).

**Data Leakage**
When information from the future, the target timestamp, or the test set leaks into training or feature generation, causing overly optimistic results (Kaufman et al., 2012; scikit-learn developers, n.d.f).

## Process Model

**QUA3CK / QUA³CK**
A structured ML process model: Question, Understanding, Algorithm Selection / Data Adaptation / Parameter Adjustment, Conclude and Compare, Knowledge Transfer (Stock et al., 2020).

**Phase Q (Question)**
Defines the problem, stakeholders, KPIs, scope, and evaluation design (Stock et al., 2020).

**Phase U (Understanding)**
Exploratory data analysis to assess structure, quality, distributions, and readiness for modeling (Stock et al., 2020).

**Phase A3 / A³**
Algorithm selection, feature adaptation or engineering, and hyperparameter adjustment (Stock et al., 2020).

**Phase C**
Conclude and compare candidate approaches, then decide on the final model (Stock et al., 2020).

**Phase K**
Knowledge transfer, documentation, and delivery artifacts (Stock et al., 2020).

## DIG Framework

**Source:**
(Su, 2025) and view [docs/project-plan-and-frameworks/DIG_framework.md](docs/project-plan-and-frameworks/DIG_framework.md)

**DIG**
A data-understanding framework used in the project docs: Description, Introspection, and Goal Setting.

**Description**
Inspect columns, samples, and basic data structure.

**Introspection**
Formulate questions, identify limitations, and validate what the data can answer.

**Goal Setting**
Decide whether data is suitable and define next steps for modeling.

## Bibliography

- Batini, C., & Scannapieco, M. (2016). Data and information quality: Dimensions, principles and techniques. Springer. https://doi.org/10.1007/978-3-319-24106-7
- Bundesnetzagentur. (n.d.). Statistiken erneuerbarer Energieträger [Data portal]. https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/EE-Statistik/start.html
- ENTSO-E. (2023). *ENTSO-E Transparency Platform* [Data platform]. European Network of Transmission System Operators for Electricity. https://transparency.entsoe.eu
- European Network of Transmission System Operators for Electricity. (n.d.). Load and consumption data. https://www.entsoe.eu/fileadmin/user_upload/_library/publications/ce/Load_and_Consumption_Data.pdf
- Global Modeling and Assimilation Office. (n.d.). Modern-Era Retrospective analysis for Research and Applications, Version 2 (MERRA-2) [Data set]. National Aeronautics and Space Administration. https://gmao.gsfc.nasa.gov/gmao-products/merra-2/
- Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and practice (3rd ed.). OTexts. https://otexts.com/fpp3/
- Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. International Journal of Forecasting, 22(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001
- Intergovernmental Panel on Climate Change. (2011). Renewable energy sources and climate change mitigation. Cambridge University Press. https://www.ipcc.ch/report/renewable-energy-sources-and-climate-change-mitigation/
- International Energy Agency. (n.d.). Solar PV. Retrieved August 2, 2026, from https://www.iea.org/energy-system/renewables/solar-pv
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. ACM Transactions on Knowledge Discovery from Data, 6(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Little, R. J. A., & Rubin, D. B. (2019). Statistical analysis with missing data (3rd ed.). Wiley.
- Makridakis, S. (1993). Accuracy measures: Theoretical and practical concerns. International Journal of Forecasting, 9(4), 527–529. https://doi.org/10.1016/0169-2070(93)90079-3
- National Institute of Standards and Technology. (2022). NIST/SEMATECH e-Handbook of statistical methods. https://doi.org/10.18434/M32189
- Open Power System Data. (n.d.). _Open Power System Data: A platform for open data of the European power system_. https://open-power-system-data.org/
- Open Power System Data. (2020a). _Data package time series_ (Version 2020-10-06) [Data set]. https://doi.org/10.25832/time_series/2020-10-06
- Open Power System Data. (2020b). _Data package weather data_ (Version 2020-09-16) [Data set]. https://doi.org/10.25832/weather_data/2020-09-16
- Python Software Foundation. (n.d.). zoneinfo— IANA time zone support [Documentation]. Retrieved August 2, 2026, from https://docs.python.org/3/library/zoneinfo.html
- Renewables.ninja. (2018). Raw weather data [Data set documentation]. https://www.renewables.ninja/news/raw-weather-data
- scikit-learn developers. (n.d.a). HistGradientBoostingRegressor [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html
- scikit-learn developers. (n.d.b). Glossary of common terms and API elements [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/glossary.html
- scikit-learn developers. (n.d.c). Metrics and scoring: Quantifying the quality of predictions [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn developers. (n.d.d). TimeSeriesSplit [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- scikit-learn developers. (n.d.e). Cross-validation: Evaluating estimator performance [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/modules/cross_validation.html
- scikit-learn developers. (n.d.f). Common pitfalls and recommended practices [Documentation]. Retrieved August 2, 2026, from https://scikit-learn.org/stable/common_pitfalls.html
- Stock, S. C., Becker, J., Grimm, D., Hotfilter, T., Molinar, G., Stang, M., & Stork, W. (2020). *QUA³CK - A machine learning development process*. In *Proceedings of Artificial Intelligence for Science, Industry and Society - PoS(AISIS2019)*, 372, Article 026. https://doi.org/10.22323/1.372.0026
- Su, J. [Jeff Su]. (2025). Master data analysis with ChatGPT (in just 12 minutes) [Video]. YouTube. https://www.youtube.com/watch?v=FKLr3ft8ea0
