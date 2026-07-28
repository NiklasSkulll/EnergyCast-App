# Core

- EnergyCast-App forecasts hourly Germany electricity load from OPSD time-series + weather data; current project framing is regression, even though some older course/prompt material mentions classification.
- QUA3CK phase workflow lives in `notebooks/`: `001_Q_Phase.ipynb`, `002_U_Phase.ipynb`, `003_A_Phase.ipynb`, `004_C_Phase.ipynb`, `005_K_Phase.ipynb`. Keep edits aligned to the active phase and do not jump ahead without user approval.
- Reusable Python is in `src/`; Streamlit entrypoint is `app/streamlit_app.py`; tests are in `tests/`; selected model artifacts are in `models/`; processed A-phase tables/checkpoints are in `data/processed/`.
- Raw data is Git LFS-backed and must remain read-only: `data/raw/time_series_60min_singleindex.csv`, `data/raw/weather_data.csv`.
- Germany focus: prefer `DE_` columns and document any deviations. Main target is `DE_load_actual_entsoe_transparency` in MW; ENTSO-E day-ahead forecast is `DE_load_forecast_entsoe_transparency`.
- Time span/constants in `src.energycast_core`: 2015-2019 local Germany panel, train years 2015-2017, validation 2018, reserved holdout/test 2019; timezone `Europe/Berlin`; join key `utc_timestamp`.
- Selected model artifact: `models/003_A_Phase_candidate_model.joblib`; metadata: `models/003_A_Phase_candidate_model_metadata.json`. Selected model is `HistGradientBoosting regressor - full lagged feature set`.
- Streamlit app is a future scenario forecast tool for 2020-2030 generated inputs, not a model-performance/reporting dashboard and not a replay of measured future truth.
- For environment/dependencies read `mem:tech_stack`; for common commands read `mem:suggested_commands`; for style and modeling invariants read `mem:conventions`; for done-checks read `mem:task_completion`.