# AGENTS Guide (EnergyCast-App)

## Purpose

This repository contains a completed QUA3CK-based data analytics project for
forecasting Germany's national hourly electricity load. Future agents should
preserve the established project story, leakage-aware evaluation design,
reproducible notebooks, reusable Python pipeline, tests, Streamlit scenario app,
and presentation artifacts.

Do not treat this as an early-phase project anymore. The five QUA3CK notebooks
have been executed and the current work is mainly maintenance, polishing,
documentation, presentation support, and carefully scoped improvements.

## Current project state

- Goal: Forecast Germany's hourly national electricity load for 2015-2019.
- Target: `DE_load_actual_entsoe_transparency`, measured in MW.
- Data sources: OPSD Time Series and OPSD Weather Data in `data/raw/`.
- Main join key: `utc_timestamp`; use local Europe/Berlin time only for calendar interpretation.
- Final selected model: `HistGradientBoosting regressor - full lagged feature set`.
- Final held-out test year: 2019.
- Final 2019 performance after refit on 2015-2018: `0.7566%` sMAPE, `540.7 MW` RMSE, `412.9 MW` MAE, `0.9970` R2.
- Streamlit app scope: future scenario forecasts for 2020-2030 timestamps from generated scenario inputs.
- Public app link is documented in `README.md`; local execution must still work via `uv run streamlit run app/streamlit_app.py`.

## Repository map

- `notebooks/001_Q_Phase.ipynb`: research question, scope, KPIs, evaluation design.
- `notebooks/002_U_Phase.ipynb`: data understanding, quality audit, time coverage, exploratory patterns.
- `notebooks/003_A_Phase.ipynb`: feature engineering, model candidates, tuning, 2018 validation selection.
- `notebooks/004_C_Phase.ipynb`: final comparison, 2019 holdout test, residual analysis, decision matrix.
- `notebooks/005_K_Phase.ipynb`: knowledge transfer, reusable app checks, Streamlit scenario validation.
- `src/energycast_core.py`: reusable data loading, feature engineering, metrics, model fitting, forecast generation.
- `src/energycast_plots.py`: Plotly chart builders.
- `app/streamlit_app.py`: Streamlit scenario forecast application.
- `models/003_A_Phase_candidate_model.joblib`: saved A-phase candidate model artifact.
- `models/003_A_Phase_candidate_model_metadata.json`: selected model metadata, features, validation metrics, hyperparameters.
- `data/processed/003_A_Phase_training_summary.csv`: A-phase training summary.
- `data/processed/003_A_Phase_validation_metrics.csv`: A-phase validation metrics.
- `tests/`: unit and smoke tests for core logic and Streamlit app structure.
- `docs/presentation_summary/`: English project overview, German HTML/PDF presentation, and German speaker notes.

## Environment and tooling

- Use `uv` for Python environment management.
- Python target is `>=3.11,<3.12`.
- Prefer the locked environment from `uv.lock`.
- Start notebooks with `uv run jupyter lab` and use the `.venv` kernel.
- Start the app locally with `uv run streamlit run app/streamlit_app.py`.
- Run tests with `uv run python -m unittest discover -s tests -v`.
- Keep dependencies minimal and justified; update `pyproject.toml` and `uv.lock` together if dependencies change.
- Raw CSVs are tracked through Git LFS; do not replace them with pointer files or partial downloads.

## Data handling rules

- Never modify `data/raw/` unless explicitly requested.
- Do not overwrite processed artifacts unless the user asks for a rerun or artifact refresh.
- Prefer Germany national `DE_` columns for Germany-focused analysis.
- Treat `DE_LU_*` and control-area columns as context-only unless a documented modeling decision says otherwise.
- Preserve the UTC-based join on `utc_timestamp`; local `cet_cest_timestamp`/Europe-Berlin time is for calendar interpretation after normalization.
- Always document missingness, duplicates, and time coverage if data-understanding work changes.
- Remember the core data facts: 43,824 hourly rows after the 2015-2019 Germany panel join; no duplicate UTC timestamps; no missing UTC hours; one missing target value at the first local timestamp.

## Leakage and modeling rules

- Preserve the chronological split logic: train on 2015-2017, validate/select on 2018, reserve 2019 for final testing.
- Do not use 2019 for model selection, hyperparameter tuning, imputation fitting, scaling fitting, or feature decisions.
- Build lagged features from past values only.
- Required historical load features: `load_lag_1h`, `load_lag_24h`, `load_lag_168h`, `load_roll24_mean_lag1`, `load_roll168_mean_lag1`.
- Weather and renewable predictors use 1-hour and 24-hour lags.
- Keep preprocessing inside scikit-learn pipelines; fit imputers/scalers only on training data.
- Treat same-hour actual weather or renewable-generation values as leakage-sensitive unless a forecast-time data-availability contract proves they are known.
- Do not describe sMAPE as "accuracy"; use "sMAPE" or "symmetric percentage error".

## Streamlit app guidance

- The app is a scenario forecast tool, not a model leaderboard dashboard.
- Future 2020-2030 outputs are scenario forecasts, not measured future truth.
- Scenario controls alter generated future inputs: demand growth, temperature shift, renewable generation scale, start date/hour, and horizon.
- Generated future feature rows come from historical seasonal profiles plus recursive load lags.
- Earlier predictions can become later lag inputs when actual future load is unavailable.
- A production version would replace generated scenario inputs with live load history plus real weather and renewable forecasts available at prediction time.
- Keep the "Assumptions" tab honest about these limitations.

## Notebook guidelines

- Keep one notebook per QUA3CK phase.
- Keep notebooks readable with concise markdown before and after important analysis blocks.
- Use `pathlib` and ensure notebooks run from the repository root.
- Favor reusable helper functions in `src/` over duplicating large logic in notebooks.
- Use Plotly for charts unless requested otherwise.
- Keep notebook outputs deterministic where possible.
- If rerunning notebooks changes metrics, update all dependent artifacts and documentation together.

## Presentation and documentation guidance

- Keep `docs/presentation_summary/Overview_summary_english.md`,
  `EnergyCast-App_presentation_german.html`, the PDF, and
  `Presentation_notes_german.md` consistent with the current model/app state.
- The German presentation is structured as 14 slides and should stay aligned with the slide-by-slide notes.
- Use "Lastprognose" or "Stromlast" rather than "Stromverbrauch" when referring to the MW target.
- Do not use "Deutschland-Stunde"; use "stündliche Beobachtung der nationalen Last in Deutschland" or "Deutschland, stündlich".
- For university presentation support, emphasize leakage-safe evaluation, data quality, model comparison, residual limitations, and scenario-app assumptions.

## Coding standards

- Keep functions small and single-purpose.
- Use explicit variable names for targets, join keys, timestamps, feature sets, metrics, and splits.
- Add brief comments only for non-obvious logic.
- Preserve existing user changes and avoid unrelated refactors.
- Use `rg` for searching and inspect context before editing.
- Use `apply_patch` for manual edits.

## Verification checklist

- For code changes, run `uv run python -m unittest discover -s tests -v`.
- For app changes, start or smoke-check `app/streamlit_app.py` when practical.
- For notebook/artifact changes, verify the affected notebook or exported artifact and update dependent docs.
- For presentation/documentation changes, verify slide counts, dates, links, and the terminology noted above.
- Before reporting completion, state what was verified and what was not run.

## Safety and reproducibility

- Avoid destructive commands unless explicitly requested.
- Preserve existing user changes unless asked to revert.
- Keep outputs deterministic where possible using fixed random seeds.
- Keep raw data immutable and large files under Git LFS.
- Keep public claims aligned with repository evidence: the final model is strong on the 2019 holdout, while the Streamlit app is a scenario demonstrator.
