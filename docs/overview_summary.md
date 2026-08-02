# Project Summary

## Overview

EnergyCast forecasts Germany's national hourly electricity load. The project addresses a supervised time-series regression problem: predict `DE_load_actual_entsoe_transparency` in MW for Germany using public Open Power System Data (OPSD) time-series data, OPSD weather data, calendar structure, renewable generation, and historical load features.

The repository follows the QUA³CK process model from problem framing to knowledge transfer. The main evidence is contained in five executed notebooks, one per phase. The implemented product combines those notebooks with reusable Python modules, saved A-phase model artifacts, processed metric tables, tests, and a Streamlit scenario forecast application.

The final selected forecasting approach is `HistGradientBoosting regressor - full lagged feature set`. In the C phase, after model selection was locked on 2018 validation data and the selected algorithm was refit on 2015-2018, it achieved `0.7566%` sMAPE, `540.7 MW` RMSE, `412.9 MW` MAE, and `0.9970` R2 on the held-out 2019 test year. The Streamlit app then turns the trained EnergyCast approach into a future scenario forecast tool for 2020-2030 timestamps.

## Phase Q — Question

The Q phase defines the project as an academic and portfolio-quality forecasting workflow for Germany's hourly electricity load. The problem context is the need for reliable load forecasts in a power system shaped by renewable generation, weather-dependent supply, calendar-driven demand, and grid balancing needs.

The research question asks to what extent machine-learning regression models can forecast Germany's hourly electricity load for 2015-2019 using weather data, renewable electricity generation, calendar effects, and historical load features while achieving an sMAPE of `5%` or below on a time-aware held-out 2019 test set.

The target variable is `DE_load_actual_entsoe_transparency`, the Germany national actual load column from the OPSD time-series dataset, measured in MW. The unit of analysis is one Germany-hour. The intended chronological split is train on 2015-2017, validate on 2018, and test once on 2019. The primary success criterion is `sMAPE <= 5%` on 2019 and improvement over a 24-hour naive persistence baseline. Supporting metrics are RMSE, MAE, and R2.

The target audience includes grid operators and energy analysts, public infrastructure planners and policymakers, students and researchers in energy analytics, and academic or portfolio reviewers. The intended outcome is a reproducible forecasting pipeline with documented model comparison, a final evaluation artifact, and an optional app-style interface for communicating or using forecasts.

One important Q-phase uncertainty remains documented in the notebooks: the exact operational forecast horizon is not fully fixed. The Q notebook explicitly notes that same-hour actual predictors are leakage-sensitive unless the final forecast creation time makes them available. Later phases reduce this risk by using lagged load, weather, and renewable-generation values, but a production deployment would still need a precise data-availability contract.

## Phase U — Understanding the Data

The project uses two raw OPSD datasets stored under `data/raw/` and tracked with Git LFS:

| Dataset | Local File | Rows | Columns | Documented Version | Role |
|---|---:|---:|---:|---|---|
| OPSD Time Series 60min singleindex | `data/raw/time_series_60min_singleindex.csv` | 50,401 | 300 | `2020-10-06` | target load, ENTSO-E forecast, renewable generation, capacity/profile fields |
| OPSD Weather Data | `data/raw/weather_data.csv` | 350,640 | 85 | `2020-09-16` | Germany-level temperature and radiation predictors |

The U notebook filters the project to Germany-local calendar years 2015-2019 and joins the time-series and weather data on `utc_timestamp`. This produces exactly `43,824` hourly rows, matching the Q-phase expectation, with no duplicate UTC timestamps and no missing UTC hours. The train/validation/test split before lag-boundary drops is `26,304` rows for 2015-2017, `8,760` rows for 2018, and `8,760` rows for 2019.

The UTC join is important because local CET/CEST wall-clock timestamps repeat during fall daylight-saving transitions. The U phase found five repeated naive local 02:00 hours across 2015-2019, so UTC is used for joining and Europe/Berlin local time is used only after normalization for calendar interpretation.

The Germany variables most relevant to the project are:

- target and reference load: `DE_load_actual_entsoe_transparency`, `DE_load_forecast_entsoe_transparency`
- weather: `DE_temperature`, `DE_radiation_direct_horizontal`, `DE_radiation_diffuse_horizontal`
- renewable generation: `DE_solar_generation_actual`, `DE_wind_generation_actual`, plus onshore/offshore wind variants in the data understanding audit
- capacity and profile fields: German solar/wind capacity and production profile columns
- context-only geography: `DE_LU_*` and German control-area columns, which are not the national `DE` target

The data quality audit supports modeling but documents several constraints. German weather is complete for the Q-period panel. The target has exactly one missing value at the first local timestamp. The ENTSO-E day-ahead forecast has `25` missing rows. Renewable generation and profile fields have small patterned gaps, for example `104` missing values in `DE_solar_generation_actual` and `75` in `DE_wind_generation_actual`. Capacity fields have `24` missing values on the final local day of 2019. `DE_LU_load_actual_entsoe_transparency` has `32,877` missing values and is treated as structural missingness tied to the Germany-Luxembourg bidding-zone definition, not as a substitute for the Germany target.

Physical range checks did not find invalid negative values in the selected Germany load, renewable, weather, or capacity fields. Profile fields can exceed `1.0` in some cases, especially offshore wind profile values, so the U notebook treats profile checks as documentation and modeling-risk signals rather than automatic deletion rules. The target itself ranges from `31,307 MW` to `77,549 MW`, with a mean of `55,859.6037 MW` over `43,823` non-missing observations.

Exploratory analysis shows the expected electricity-load structure: higher weekday than weekend load, a daily ramp-up and daytime plateau, and higher average load in colder months (view "Monthly mean German load, 2015-2019", "002_U_Phase.ipynb, Interpretation: The target shows higher weekday load than weekend load, a clear daily ramp-up and daytime plateau, and higher average load in colder months") (view "Mean load by month and weekday/weekend", "002_U_Phase.ipynb, Interpretation: The target shows higher weekday load than weekend load, a clear daily ramp-up and daytime plateau, and higher average load in colder months") (view "Mean German load by weekday and local hour", "002_U_Phase.ipynb, Interpretation: The target shows higher weekday load than weekend load, a clear daily ramp-up and daytime plateau, and higher average load in colder months"). Yearly mean target load ranges from `54,738.4567 MW` in 2015 to `56,951.3477 MW` in 2018, with 2019 at `55,990.3318 MW`.

The U phase also quantifies predictor signal. Simple Pearson correlation with the target is very strong for `DE_load_forecast_entsoe_transparency` (`0.9790`) and weaker for many same-hour weather and renewable variables. Temperature has a simple linear correlation of `-0.0272`, which the notebook interprets as evidence that temperature effects are nonlinear and confounded with season and calendar structure (view "Target load vs Germany temperature (sampled)", "002_U_Phase.ipynb, Interpretation: Simple linear weather correlations are limited, especially for temperature, which is consistent with heating and cooling effects being nonlinear and confounded with season and calendar structure") (view "Simple Pearson correlation with target load", "002_U_Phase.ipynb, Interpretation: Solar and radiation variables show moderate positive correlation because daytime and seasonal structure overlap with load; correlations are orientation only, not final feature importance"). Lagged load is much stronger: `load_lag_1h` correlates `0.9662`, `load_lag_24h` correlates `0.7573`, and `load_lag_168h` correlates `0.9105` with the target.

The U-phase 2018 reference metrics provide expectations before model training: ENTSO-E day-ahead forecast reaches `2.7964%` sMAPE and `1,577.0950 MW` MAE; 168-hour weekly persistence reaches `4.5431%` sMAPE and `2,555.6789 MW` MAE; 24-hour naive persistence reaches `8.3684%` sMAPE and `4,607.9002 MW` MAE. The 2019 year remains reserved at this point.

## Phase A³ — Algorithm Development and Optimization

### Algorithm Selection

The A³ phase turns the Q and U findings into a leakage-aware regression experiment. It evaluates simple baselines, regularized linear models, instance-based learning, scalable support-vector regression, individual trees, ensemble trees, and boosted tree models. This candidate set is appropriate because the project needs both interpretable reference points and nonlinear models that can capture daily, weekly, seasonal, weather, and renewable interactions.

The evaluated trained candidates are:

- `Dummy mean regressor`
- `Ridge regression - calendar only`
- `Ridge regression - calendar + load lags`
- `Ridge regression - full lagged feature set`
- `KNN regressor - full lagged feature set`
- `Linear SVR - full lagged feature set`
- `Decision Tree regressor - full lagged feature set`
- `Random Forest regressor - full lagged feature set`
- `HistGradientBoosting regressor - full lagged feature set`
- `XGBoost regressor - full lagged feature set`

The A phase also compares against non-trained reference forecasts: 24-hour naive persistence, 168-hour weekly persistence, and the ENTSO-E day-ahead forecast.

After dropping the first lag-boundary rows and the first missing target row, the modeling table has `43,655` rows. A³ uses `26,135` rows for training on 2015-2017, `8,760` rows for validation on 2018, and keeps `8,760` rows for the reserved 2019 C-phase test.

### Adapting Features

Feature engineering follows the U-phase leakage audit. Calendar features are derived from timestamps and encoded cyclically for hour, weekday, and month, plus `is_weekend`. Historical load features are shifted before use: `load_lag_1h`, `load_lag_24h`, `load_lag_168h`, `load_roll24_mean_lag1`, and `load_roll168_mean_lag1`. Weather and renewable predictors are also shifted, using 1-hour and 24-hour lags for Germany temperature, direct radiation, diffuse radiation, solar generation, and total wind generation.

The selected full feature set contains `22` columns: `7` calendar features, `5` load lag or rolling-load features, `6` lagged weather features, and `4` lagged renewable-generation features. Optional missing predictor cells remain for the pipeline imputer, especially lagged solar and wind generation gaps, while required target and load-lag rows are dropped before supervised fitting.

Preprocessing is kept inside scikit-learn pipelines. Median imputation is fitted only on the training data within each model pipeline. Scaling is applied where needed for models such as Ridge, Linear SVR, and KNN, rather than being applied globally before the split.

### Adjusting Hyperparameters

The A phase uses chronological `TimeSeriesSplit(n_splits=3)` with `GridSearchCV` and sMAPE as the validation scorer. Model selection is fixed before 2019: choose the lowest 2018 validation sMAPE, using RMSE as a tie-breaker.

The selected A-phase model is `HistGradientBoosting regressor - full lagged feature set`. Its best saved parameters are:

| Parameter | Value |
|---|---:|
| `model__max_iter` | `400` |
| `model__learning_rate` | `0.05` |
| `model__max_leaf_nodes` | `31` |
| `model__l2_regularization` | `0.0` |

On 2018 validation, this model achieves `0.7420%` sMAPE, `553.3419 MW` RMSE, `412.2465 MW` MAE, and `0.9969` R2. It also has the best cross-validation mean sMAPE among the A-phase candidates at `0.8143%`. The next strongest validation models are XGBoost at `0.7885%` sMAPE and Random Forest at `0.8623%` sMAPE (view "2018 validation sMAPE by A-phase regression candidate", "003_A_Phase.ipynb, Chart compares A-phase regression candidates on 2018 validation sMAPE against the Q-phase 5% KPI threshold") (view "2018 validation comparison: trained candidates and reference forecasts", "003_A_Phase.ipynb, Chart compares trained candidates and reference forecasts on the 2018 validation year").

Permutation importance in the A notebook shows `load_lag_1h` as the dominant feature, with a validation RMSE increase of `12,497.2617` when shuffled. Hour-of-day encodings, weekly lag, and lagged solar/weather features also contribute. This supports the Q-phase hypothesis that historical load dominates short-term load forecasting (view "Top validation permutation importances: HistGradientBoosting regressor - full lagged feature set", "003_A_Phase.ipynb, Interpretation: The selected model relies most strongly on recent load history; calendar, weather and renewable lags add nonlinear context but do not replace historical load as the main signal").

The A phase writes the model handoff artifacts:

- `data/processed/003_A_Phase_training_summary.csv`
- `data/processed/003_A_Phase_validation_metrics.csv`
- `models/003_A_Phase_candidate_model.joblib`
- `models/003_A_Phase_candidate_model_metadata.json`

## Phase C — Conclude & Compare

The C phase rebuilds the same leakage-aware data and validates the A-phase decision. It first confirms the 2018 validation ranking, then locks the model selection and refits trained candidates on 2015-2018 before evaluating once on 2019.

The selected approach performs best on the held-out 2019 test year. It meets the Q-phase acceptance threshold and beats all repository baselines and reference forecasts in the final comparison (view "2019 final test sMAPE after refit on 2015-2018", "004_C_Phase.ipynb, Final 2019 test evaluation: models are refit on 2015-2018 after selection is locked; the 2019 table is evidence for the conclusion, not a second tuning round").

| Model or Approach | Main Metrics | Strengths | Limitations |
|---|---:|---|---|
| `HistGradientBoosting regressor - full lagged feature set` | `0.7566%` sMAPE, `540.7 MW` RMSE, `412.9 MW` MAE, `0.9970` R2 | Best 2019 performance; strong validation-to-test stability; reproducible scikit-learn pipeline | Less directly interpretable than linear baselines; still depends on lagged actual weather and renewable inputs |
| `XGBoost regressor - full lagged feature set` | `0.7769%` sMAPE, `554.0 MW` RMSE, `423.0 MW` MAE, `0.9969` R2 | Nearly as accurate as the selected model; fast prediction | Adds dependency and slightly weaker weighted decision score |
| `Random Forest regressor - full lagged feature set` | `0.8018%` sMAPE, `581.7 MW` RMSE, `437.9 MW` MAE, `0.9965` R2 | Strong nonlinear benchmark | Higher inference cost than boosted alternatives |
| `Decision Tree regressor - full lagged feature set` | `1.0792%` sMAPE, `804.9 MW` RMSE, `585.5 MW` MAE, `0.9934` R2 | Interpretable nonlinear model | Less accurate than ensemble methods |
| `Ridge regression - full lagged feature set` | `2.1496%` sMAPE, `1,546.7 MW` RMSE, `1,174.7 MW` MAE, `0.9756` R2 | Simple, fast, stable | Cannot capture nonlinear structure as well as boosted trees |
| `Linear SVR - full lagged feature set` | `2.1752%` sMAPE, `1,665.8 MW` RMSE, `1,197.4 MW` MAE, `0.9716` R2 | Scaled linear support-vector regression candidate | Weaker than tree-based models |
| `Ridge regression - calendar + load lags` | `2.3472%` sMAPE, `1,725.0 MW` RMSE, `1,296.3 MW` MAE, `0.9696` R2 | Shows the value of historical load with a simple model | Omits lagged weather and renewable context |
| `KNN regressor - full lagged feature set` | `2.3580%` sMAPE, `1,887.4 MW` RMSE, `1,275.6 MW` MAE, `0.9636` R2 | Instance-based comparison point | Lowest deployment suitability in the decision matrix due to prediction cost |
| `ENTSO-E day-ahead forecast` | `3.5864%` sMAPE, `2,489.2 MW` RMSE, `1,988.9 MW` MAE, `0.9367` R2 | Strong external reference forecast | Not an in-repository trained model and weaker than selected ML candidates |
| `168h weekly naive persistence` | `4.6812%` sMAPE, `4,464.9 MW` RMSE, `2,558.0 MW` MAE, `0.7963` R2 | Simple and surprisingly strong weekly baseline | Much worse than trained lagged models |
| `Ridge regression - calendar only` | `7.6124%` sMAPE, `5,326.8 MW` RMSE, `4,145.7 MW` MAE, `0.7100` R2 | Tests calendar-only signal and slightly beats 24-hour naive on 2019 sMAPE | Fails the `5%` acceptance threshold |
| `24h naive persistence` | `8.4171%` sMAPE, `6,944.0 MW` RMSE, `4,557.5 MW` MAE, `0.5072` R2 | Required Q-phase baseline | Far below selected model performance |
| `Dummy mean regressor` | `15.5745%` sMAPE, `9,893.0 MW` RMSE, `8,618.2 MW` MAE, `-0.0002` R2 | Sanity baseline | Does not model time structure |

The selected model reduces 2019 sMAPE by `91.0115%` relative to 24-hour naive persistence, by `83.8381%` relative to 168-hour weekly persistence, and by `78.9046%` relative to the ENTSO-E day-ahead forecast. The C-phase KPI table marks all required criteria as passed: sMAPE below `5%`, improvement over the 24-hour naive baseline, no use of 2019 for model selection, and past-only predictor construction.

The residual analysis shows a small mean bias of `-13.6282 MW`, median absolute error of `328.2813 MW`, 95th percentile absolute error of `1,070.5073 MW`, and maximum absolute error of `4,779.3221 MW`. All monthly sMAPE values are well below the `5%` threshold. December is the highest-error month at `0.9061%` sMAPE, while July is lowest at `0.6000%`. Errors are higher around the morning ramp, especially hour `6` at `1.1815%` sMAPE and hour `5` at `1.0538%`. Weekend sMAPE is `0.8561%`, compared with `0.7169%` for weekdays (view "Selected model fit on a two-week 2019 slice: HistGradientBoosting regressor - full lagged feature set", "004_C_Phase.ipynb, Residual and robustness analysis inspects whether a single annual metric hides systematic errors") (view "Selected model residual distribution on 2019 test year", "004_C_Phase.ipynb, Residual interpretation: the selected model's average bias is small relative to national hourly load") (view "Selected model 2019 sMAPE by month", "004_C_Phase.ipynb, Residual interpretation: all monthly sMAPE values stay well below the Q-phase 5% threshold").

The weighted C-phase decision matrix also selects HistGradientBoosting, with a weighted score of `4.5000`. XGBoost scores `4.3000`, while Random Forest and Ridge with calendar plus load lags each score `4.2000`. The final choice is therefore not only the lowest-error model, but also a maintainable, reproducible, deployment-suitable option inside the repository's Python and scikit-learn stack (view "Weighted C-phase decision score", "004_C_Phase.ipynb, Decision matrix combines predictive performance with generalization, inference cost, interpretability, complexity, maintainability, reproducibility and deployment suitability").

The main limitations are still important. The final model uses lagged actual weather and renewable-generation values, which are safe for the retrospective past-only setup used here but require reliable availability or forecast substitutes in a live deployment. Public holidays were proposed in Q but no documented holiday source was added. The repository validates 2019 but does not prove performance for later years without additional measured target data.

## Phase K — Knowledge Transfer

The K phase converts the modeling work into a usable Streamlit scenario forecast application. The app is intentionally forecast-first: it does not duplicate the C-phase model leaderboard as the main product. Instead, it lets users select a future forecast start date, start hour, horizon, and scenario assumptions, then generates future feature rows and calls the selected model to forecast Germany national hourly load.

The Streamlit app supports future timestamps from 2020 through 2030. Its sidebar controls include:

- forecast start date and start hour
- horizon choices: next 24 hours, next 48 hours, next 7 days, and next 30 days
- demand growth per year in percent
- temperature shift in degrees C
- renewable generation scale in percent
- a toggle to show generated input columns in the forecast table

The app has three tabs: `Scenario Forecast`, `Generated Inputs`, and `Assumptions`. The main tab shows peak forecast, peak hour, average forecast, forecasted energy, an hourly forecast curve, and a forecast table. The generated-inputs tab shows the lagged load, generated weather, and generated renewable inputs behind the selected forecast. The assumptions tab explains that 2020+ outputs are scenario forecasts, not measured future truth (view "Forecasted electricity load", "005_K_Phase.ipynb, Implemented forecast checks: the Streamlit app uses the same scenario forecast helper and Plotly chart builders") (view "Recent-load inputs used by the forecast", "005_K_Phase.ipynb, Implemented forecast checks: the Streamlit app uses the same scenario forecast helper and Plotly chart builders").

The reusable implementation builds the same project panel from raw OPSD CSVs, creates the same lagged feature structure, refits the locked selected HistGradientBoosting configuration on 2015-2018 for 2019 checks, and generates future scenario rows from historical seasonal profiles. When future actual load is not available, earlier model predictions recursively become later load-lag inputs. This makes the app practical for demonstration while keeping the scenario assumptions visible.

The K notebook validates that the reusable app pipeline reproduces the C-phase selected-model metrics within tight tolerance:

| Check | Expected | Observed | Status |
|---|---:|---:|---|
| selected 2019 sMAPE | `0.7566` | `0.756574` | pass |
| selected 2019 RMSE | `540.7388` | `540.738843` | pass |
| selected 2019 MAE | `412.8741` | `412.874059` | pass |
| selected 2019 R2 | `0.9970` | `0.997012` | pass |

It also validates a sample 24-hour future scenario beginning on `2026-07-28`: the forecast returns `24` hourly rows, contains no actual target column, and produces a non-null peak load of `69,536.434822 MW` at `2026-07-28 11:00:00+02:00`.

Reproducibility is supported by `pyproject.toml`, `uv.lock`, Git LFS tracking for large CSV, notebook, and model artifacts, the executed phase notebooks, saved model metadata, processed validation/training summaries, and unit/smoke tests. The tests cover sMAPE calculation, leakage-safe lag construction, reference forecast evaluation, date and KPI filtering, future scenario feature generation, scenario-control effects, and Streamlit rendering as a scenario forecast tool.

No public deployment URL is present in the repository. The README documents local execution with `uv run streamlit run app/streamlit_app.py`, and its Streamlit app link is empty. Therefore, the finished-product link below keeps the required placeholder.

Recommended next steps are to define the production forecast horizon explicitly, replace generated future inputs with live load history plus weather and renewable forecasts, add a documented German holiday feature if desired, validate the model on post-2019 measured target data, and decide whether the app should load a persisted deployment artifact or continue refitting the locked selected estimator from the reproducible raw-data pipeline.

# Finished Product

**Open the Streamlit application:** [https://energycast-app.streamlit.app/](https://energycast-app.streamlit.app/)
