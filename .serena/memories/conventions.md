# Conventions

- Use pathlib for paths; notebooks and app should resolve/run from repo root. `src.energycast_core.resolve_project_root()` finds a root containing `pyproject.toml` and `data/`.
- Keep notebooks readable: brief markdown around analysis blocks; reusable helpers for repeated logic; deterministic seeds such as `RANDOM_STATE = 42`.
- Do not write under `data/` unless explicitly requested. Raw data is never modified; `data/interim/` and `data/processed/` are only for requested intermediate/processed artifacts.
- Feature engineering must be leakage-safe: load, weather, and renewable predictors use past lags; recursive future forecasts may feed previous predictions into later load lags.
- Canonical feature families: cyclical calendar features, load lags/rolling lag means, DE weather lags, DE solar/wind generation lags. Full feature list is `FULL_LAGGED_FEATURES` in `src.energycast_core`.
- Evaluation metrics for the regression target: sMAPE, RMSE, MAE, R2. Primary selection metric is sMAPE with RMSE tie-breaker.
- Streamlit app copy/tests guard the boundary: first screen is `EnergyCast Scenario Forecast`, tabs are `Scenario Forecast`, `Generated Inputs`, `Assumptions`; avoid turning it into a 2019 model-statistics dashboard.
- Code style: small single-purpose functions, explicit target/join-key variable names, type hints where useful, and comments only for non-obvious logic.