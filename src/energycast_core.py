from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import time as datetime_time
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

JOIN_KEY = "utc_timestamp"
SOURCE_LOCAL_TIMESTAMP_COL = "cet_cest_timestamp"
LOCAL_TIMESTAMP = "local_timestamp"
LOCAL_TZ = "Europe/Berlin"

TARGET = "DE_load_actual_entsoe_transparency"
REFERENCE_FORECAST = "DE_load_forecast_entsoe_transparency"

Q_START_YEAR = 2015
Q_END_YEAR = 2019
TRAIN_YEARS = [2015, 2016, 2017]
VALIDATION_YEAR = 2018
TEST_YEAR = 2019
RANDOM_STATE = 42
EXPECTED_Q_ROWS = 43_824
EXPECTED_MODEL_ROWS = 43_655

SELECTED_MODEL_NAME = "HistGradientBoosting regressor - full lagged feature set"
SELECTED_FEATURE_SET = "full lagged feature set"

WEATHER_DE_COLS = [
    "DE_temperature",
    "DE_radiation_direct_horizontal",
    "DE_radiation_diffuse_horizontal",
]
RENEWABLE_LAG_SOURCE_COLS = [
    "DE_solar_generation_actual",
    "DE_wind_generation_actual",
]
TIME_SERIES_SELECTED_COLS = [
    JOIN_KEY,
    SOURCE_LOCAL_TIMESTAMP_COL,
    TARGET,
    REFERENCE_FORECAST,
    *RENEWABLE_LAG_SOURCE_COLS,
]
WEATHER_SELECTED_COLS = [JOIN_KEY, *WEATHER_DE_COLS]

CALENDAR_FEATURES = [
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos",
    "month_sin",
    "month_cos",
    "is_weekend",
]
LOAD_FEATURES = [
    "load_lag_1h",
    "load_lag_24h",
    "load_lag_168h",
    "load_roll24_mean_lag1",
    "load_roll168_mean_lag1",
]
WEATHER_LAG_FEATURES = [f"{col}_lag{lag}h" for col in WEATHER_DE_COLS for lag in [1, 24]]
RENEWABLE_LAG_FEATURES = [f"{col}_lag{lag}h" for col in RENEWABLE_LAG_SOURCE_COLS for lag in [1, 24]]
FULL_LAGGED_FEATURES = [*CALENDAR_FEATURES, *LOAD_FEATURES, *WEATHER_LAG_FEATURES, *RENEWABLE_LAG_FEATURES]

FEATURE_SETS = {
    "calendar only": CALENDAR_FEATURES,
    "calendar + load lags": [*CALENDAR_FEATURES, *LOAD_FEATURES],
    "full lagged feature set": FULL_LAGGED_FEATURES,
}

REFERENCE_PREDICTION_COLUMNS = {
    "24h naive persistence": "load_lag_24h",
    "168h weekly naive persistence": "load_lag_168h",
    "ENTSO-E day-ahead forecast": REFERENCE_FORECAST,
}


@dataclass(frozen=True)
class ForecastBundle:
    metadata: dict
    validation_metrics: pd.DataFrame
    model_data: pd.DataFrame
    forecast_frame: pd.DataFrame
    selected_estimator: Pipeline
    test_summary: pd.DataFrame
    selected_metrics: dict[str, float | int | str]
    benchmark_improvements: pd.DataFrame
    residual_summary: pd.DataFrame
    monthly_error: pd.DataFrame
    hourly_error: pd.DataFrame
    day_type_error: pd.DataFrame
    panel_audit: pd.DataFrame
    feature_audit: pd.DataFrame


@dataclass(frozen=True)
class ScenarioSettings:
    demand_growth_pct_per_year: float = 0.5
    temperature_shift_c: float = 0.0
    renewable_generation_scale_pct: float = 100.0


def resolve_project_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "data").exists():
            return candidate
    raise FileNotFoundError("Could not resolve the EnergyCast project root from the current path.")


def project_paths(root: str | Path | None = None) -> dict[str, Path]:
    base = resolve_project_root(root)
    return {
        "root": base,
        "time_series": base / "data" / "raw" / "time_series_60min_singleindex.csv",
        "weather": base / "data" / "raw" / "weather_data.csv",
        "validation_metrics": base / "data" / "processed" / "003_A_Phase_validation_metrics.csv",
        "training_summary": base / "data" / "processed" / "003_A_Phase_training_summary.csv",
        "model_metadata": base / "models" / "003_A_Phase_candidate_model_metadata.json",
    }


def add_local_timestamp(frame: pd.DataFrame, timestamp_col: str = JOIN_KEY) -> pd.DataFrame:
    prepared = frame.copy()
    prepared[timestamp_col] = pd.to_datetime(prepared[timestamp_col], utc=True)
    prepared[LOCAL_TIMESTAMP] = prepared[timestamp_col].dt.tz_convert(LOCAL_TZ)
    return prepared


def add_cyclical_feature(frame: pd.DataFrame, source_col: str, period: int, prefix: str) -> pd.DataFrame:
    prepared = frame.copy()
    prepared[f"{prefix}_sin"] = np.sin(2 * np.pi * prepared[source_col] / period)
    prepared[f"{prefix}_cos"] = np.cos(2 * np.pi * prepared[source_col] / period)
    return prepared


def load_phase_metadata(root: str | Path | None = None) -> dict:
    path = project_paths(root)["model_metadata"]
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_validation_metrics(root: str | Path | None = None) -> pd.DataFrame:
    frame = pd.read_csv(project_paths(root)["validation_metrics"])
    return frame.sort_values(["sMAPE_pct", "RMSE_MW"]).reset_index(drop=True)


def load_panel(root: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = project_paths(root)
    time_series = pd.read_csv(paths["time_series"], usecols=TIME_SERIES_SELECTED_COLS)
    weather = pd.read_csv(paths["weather"], usecols=WEATHER_SELECTED_COLS)

    time_series = add_local_timestamp(time_series)
    weather = add_local_timestamp(weather)

    time_series_q = time_series[time_series[LOCAL_TIMESTAMP].dt.year.between(Q_START_YEAR, Q_END_YEAR)].copy()
    weather_q = weather[weather[LOCAL_TIMESTAMP].dt.year.between(Q_START_YEAR, Q_END_YEAR)].copy()

    panel = (
        time_series_q.drop(columns=[LOCAL_TIMESTAMP])
        .merge(weather_q.drop(columns=[LOCAL_TIMESTAMP]), on=JOIN_KEY, how="inner")
        .sort_values(JOIN_KEY)
        .reset_index(drop=True)
    )
    panel[LOCAL_TIMESTAMP] = panel[JOIN_KEY].dt.tz_convert(LOCAL_TZ)
    panel["year"] = panel[LOCAL_TIMESTAMP].dt.year
    panel["month"] = panel[LOCAL_TIMESTAMP].dt.month
    panel["weekday_number"] = panel[LOCAL_TIMESTAMP].dt.weekday
    panel["hour"] = panel[LOCAL_TIMESTAMP].dt.hour
    panel["is_weekend"] = (panel["weekday_number"] >= 5).astype(int)

    audit = pd.DataFrame(
        [
            {"check": "joined Germany-local 2015-2019 rows", "value": len(panel), "expected": EXPECTED_Q_ROWS},
            {"check": "duplicate UTC timestamps", "value": int(panel[JOIN_KEY].duplicated().sum()), "expected": 0},
            {"check": "missing target rows", "value": int(panel[TARGET].isna().sum()), "expected": 1},
            {"check": "missing Germany weather cells", "value": int(panel[WEATHER_DE_COLS].isna().sum().sum()), "expected": 0},
            {"check": "first local timestamp", "value": str(panel[LOCAL_TIMESTAMP].min()), "expected": "2015-01-01 00:00:00+01:00"},
            {"check": "last local timestamp", "value": str(panel[LOCAL_TIMESTAMP].max()), "expected": "2019-12-31 23:00:00+01:00"},
        ]
    )
    return panel, audit


def _ensure_calendar_columns(frame: pd.DataFrame) -> pd.DataFrame:
    prepared = frame.copy()
    if LOCAL_TIMESTAMP not in prepared.columns:
        prepared = add_local_timestamp(prepared)
    if "year" not in prepared.columns:
        prepared["year"] = prepared[LOCAL_TIMESTAMP].dt.year
    if "month" not in prepared.columns:
        prepared["month"] = prepared[LOCAL_TIMESTAMP].dt.month
    if "weekday_number" not in prepared.columns:
        prepared["weekday_number"] = prepared[LOCAL_TIMESTAMP].dt.weekday
    if "hour" not in prepared.columns:
        prepared["hour"] = prepared[LOCAL_TIMESTAMP].dt.hour
    if "is_weekend" not in prepared.columns:
        prepared["is_weekend"] = (prepared["weekday_number"] >= 5).astype(int)
    return prepared


def build_features(panel: pd.DataFrame) -> pd.DataFrame:
    features = _ensure_calendar_columns(panel)
    features = add_cyclical_feature(features, "hour", 24, "hour")
    features = add_cyclical_feature(features, "weekday_number", 7, "weekday")
    features = add_cyclical_feature(features, "month", 12, "month")

    for lag in [1, 24, 168]:
        features[f"load_lag_{lag}h"] = features[TARGET].shift(lag)

    features["load_roll24_mean_lag1"] = features[TARGET].shift(1).rolling(window=24, min_periods=24).mean()
    features["load_roll168_mean_lag1"] = features[TARGET].shift(1).rolling(window=168, min_periods=168).mean()

    for source_col in [*WEATHER_DE_COLS, *RENEWABLE_LAG_SOURCE_COLS]:
        for lag in [1, 24]:
            features[f"{source_col}_lag{lag}h"] = features[source_col].shift(lag)

    return features


def build_model_data(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = build_features(panel)
    required_complete_columns = [TARGET, *LOAD_FEATURES]
    model_data = features.dropna(subset=required_complete_columns).copy()
    model_data["day_type"] = np.where(model_data["is_weekend"].eq(1), "weekend", "weekday")

    feature_audit = pd.DataFrame(
        [
            {"item": "raw joined rows", "value": len(panel)},
            {"item": "modeling rows after target and lag boundary drops", "value": len(model_data)},
            {"item": "calendar features", "value": len(CALENDAR_FEATURES)},
            {"item": "load lag and rolling features", "value": len(LOAD_FEATURES)},
            {"item": "lagged weather features", "value": len(WEATHER_LAG_FEATURES)},
            {"item": "lagged renewable features", "value": len(RENEWABLE_LAG_FEATURES)},
            {
                "item": "optional missing predictor cells handled by pipeline imputers",
                "value": int(model_data[FULL_LAGGED_FEATURES].isna().sum().sum()),
            },
        ]
    )
    return model_data, feature_audit


def smape(y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray) -> float:
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)
    denominator = np.abs(actual) + np.abs(predicted)
    valid = denominator != 0
    if not np.any(valid):
        return 0.0
    return float(np.mean(2 * np.abs(actual[valid] - predicted[valid]) / denominator[valid]) * 100)


def regression_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: pd.Series | np.ndarray,
    rows: int | None = None,
) -> dict[str, float | int]:
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)
    return {
        "rows": int(rows if rows is not None else len(actual)),
        "sMAPE_pct": smape(actual, predicted),
        "RMSE_MW": float(np.sqrt(np.mean((actual - predicted) ** 2))),
        "MAE_MW": float(mean_absolute_error(actual, predicted)),
        "R2": float(r2_score(actual, predicted)),
    }


def format_metric_table(frame: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    formatted = frame.copy()
    numeric_cols = [
        "sMAPE_pct",
        "RMSE_MW",
        "MAE_MW",
        "R2",
        "bias_MW",
        "absolute_error_MW",
        "residual_MW",
        "train_seconds",
        "predict_seconds",
        "ms_per_1000_rows",
        "relative_sMAPE_reduction_pct",
    ]
    for col in numeric_cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].astype(float).round(digits)
    return formatted


def evaluate_reference_forecasts(frame: pd.DataFrame, split_name: str) -> pd.DataFrame:
    reference_specs = [
        ("24h naive persistence", "24-hour persistence baseline", "load_lag_24h"),
        ("168h weekly naive persistence", "weekly persistence baseline", "load_lag_168h"),
        ("ENTSO-E day-ahead forecast", "external reference forecast", REFERENCE_FORECAST),
    ]
    rows = []
    for candidate, candidate_type, prediction_col in reference_specs:
        valid = frame[[TARGET, prediction_col]].dropna()
        start = time.perf_counter()
        y_pred = valid[prediction_col].to_numpy(dtype=float)
        predict_seconds = time.perf_counter() - start
        row = {
            "candidate": candidate,
            "candidate_type": candidate_type,
            "feature_set": "reference column",
            "split": split_name,
            "hyperparameters": "not trained",
            "train_seconds": 0.0,
            "predict_seconds": predict_seconds,
            "ms_per_1000_rows": predict_seconds / max(len(valid), 1) * 1_000_000,
        }
        row.update(regression_metrics(valid[TARGET], y_pred, rows=len(valid)))
        rows.append(row)
    return pd.DataFrame(rows)


def numeric_regression_pipeline(model, *, scale: bool = False) -> Pipeline:
    steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", model))
    return Pipeline(steps)


def selected_model_pipeline() -> Pipeline:
    return numeric_regression_pipeline(
        HistGradientBoostingRegressor(
            max_iter=400,
            learning_rate=0.05,
            max_leaf_nodes=31,
            l2_regularization=0.0,
            random_state=RANDOM_STATE,
        )
    )


def compact_model_registry() -> pd.DataFrame:
    rows = [
        {
            "candidate": "Dummy mean regressor",
            "candidate_type": "statistical baseline",
            "feature_set": SELECTED_FEATURE_SET,
            "pipeline": Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", DummyRegressor(strategy="mean"))]),
            "features": FULL_LAGGED_FEATURES,
        },
        {
            "candidate": "Ridge regression - calendar + load lags",
            "candidate_type": "ML regressor",
            "feature_set": "calendar + load lags",
            "pipeline": numeric_regression_pipeline(Ridge(alpha=100.0), scale=True),
            "features": FEATURE_SETS["calendar + load lags"],
        },
        {
            "candidate": SELECTED_MODEL_NAME,
            "candidate_type": "ML regressor",
            "feature_set": SELECTED_FEATURE_SET,
            "pipeline": selected_model_pipeline(),
            "features": FULL_LAGGED_FEATURES,
        },
    ]
    return pd.DataFrame(rows)


def fit_selected_model(model_data: pd.DataFrame) -> Pipeline:
    train_validation_df = model_data[model_data["year"].between(TRAIN_YEARS[0], VALIDATION_YEAR)].copy()
    estimator = selected_model_pipeline()
    estimator.fit(train_validation_df[FULL_LAGGED_FEATURES], train_validation_df[TARGET])
    return estimator


def selected_forecast_frame(model_data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float | int | str], float, Pipeline]:
    train_validation_df = model_data[model_data["year"].between(TRAIN_YEARS[0], VALIDATION_YEAR)].copy()
    test_df = model_data[model_data["year"].eq(TEST_YEAR)].copy()
    estimator = selected_model_pipeline()
    start = time.perf_counter()
    estimator.fit(train_validation_df[FULL_LAGGED_FEATURES], train_validation_df[TARGET])
    train_seconds = time.perf_counter() - start
    start = time.perf_counter()
    predictions = estimator.predict(test_df[FULL_LAGGED_FEATURES])
    predict_seconds = time.perf_counter() - start

    forecast_columns = [
        JOIN_KEY,
        LOCAL_TIMESTAMP,
        TARGET,
        REFERENCE_FORECAST,
        "year",
        "month",
        "weekday_number",
        "hour",
        "is_weekend",
        "day_type",
        "load_lag_1h",
        "load_lag_24h",
        "load_lag_168h",
        "load_roll24_mean_lag1",
        "load_roll168_mean_lag1",
        "DE_temperature_lag1h",
        "DE_temperature_lag24h",
        "DE_solar_generation_actual_lag1h",
        "DE_solar_generation_actual_lag24h",
        "DE_wind_generation_actual_lag1h",
        "DE_wind_generation_actual_lag24h",
    ]
    forecast = test_df[[col for col in forecast_columns if col in test_df.columns]].copy()
    forecast["prediction_MW"] = predictions
    forecast["residual_MW"] = forecast[TARGET] - forecast["prediction_MW"]
    forecast["absolute_error_MW"] = forecast["residual_MW"].abs()
    forecast["absolute_sMAPE_pct"] = (
        2
        * forecast["absolute_error_MW"]
        / (forecast[TARGET].abs() + forecast["prediction_MW"].abs())
        * 100
    )

    metrics = {
        "candidate": SELECTED_MODEL_NAME,
        "candidate_type": "ML regressor",
        "feature_set": SELECTED_FEATURE_SET,
        "split": "test",
        "hyperparameters": "max_iter=400, learning_rate=0.05, max_leaf_nodes=31, l2_regularization=0.0",
        "train_seconds": train_seconds,
        "predict_seconds": predict_seconds,
        "ms_per_1000_rows": predict_seconds / max(len(test_df), 1) * 1_000_000,
    }
    metrics.update(regression_metrics(test_df[TARGET], predictions, rows=len(test_df)))
    return forecast, metrics, train_seconds, estimator


def grouped_error_summary(frame: pd.DataFrame, group_col: str) -> pd.DataFrame:
    rows = []
    for group_value, group in frame.groupby(group_col, sort=True):
        rows.append(
            {
                group_col: group_value,
                "rows": len(group),
                "sMAPE_pct": smape(group[TARGET], group["prediction_MW"]),
                "MAE_MW": float(mean_absolute_error(group[TARGET], group["prediction_MW"])),
                "bias_MW": float((group[TARGET] - group["prediction_MW"]).mean()),
            }
        )
    return pd.DataFrame(rows)


def residual_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    residual_values = frame["residual_MW"].to_numpy(dtype=float)
    durbin_watson = float(np.sum(np.diff(residual_values) ** 2) / np.sum(residual_values**2))
    lag1_residual_autocorr = float(pd.Series(residual_values).autocorr(lag=1))
    return pd.DataFrame(
        [
            {"diagnostic": "mean residual / bias", "value": frame["residual_MW"].mean(), "unit": "MW"},
            {"diagnostic": "median absolute error", "value": frame["absolute_error_MW"].median(), "unit": "MW"},
            {"diagnostic": "95th percentile absolute error", "value": frame["absolute_error_MW"].quantile(0.95), "unit": "MW"},
            {"diagnostic": "maximum absolute error", "value": frame["absolute_error_MW"].max(), "unit": "MW"},
            {"diagnostic": "residual standard deviation", "value": frame["residual_MW"].std(), "unit": "MW"},
            {"diagnostic": "Durbin-Watson statistic", "value": durbin_watson, "unit": "unitless"},
            {"diagnostic": "lag-1 residual autocorrelation", "value": lag1_residual_autocorr, "unit": "unitless"},
        ]
    )


def benchmark_improvements(selected_metrics: dict[str, float | int | str], reference_metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    selected_smape = float(selected_metrics["sMAPE_pct"])
    for baseline_name in ["24h naive persistence", "168h weekly naive persistence", "ENTSO-E day-ahead forecast"]:
        baseline = reference_metrics[reference_metrics["candidate"].eq(baseline_name)].iloc[0]
        baseline_smape = float(baseline["sMAPE_pct"])
        rows.append(
            {
                "comparison": f"selected model vs {baseline_name}",
                "baseline_sMAPE_pct": baseline_smape,
                "selected_sMAPE_pct": selected_smape,
                "relative_sMAPE_reduction_pct": (baseline_smape - selected_smape) / baseline_smape * 100,
            }
        )
    return pd.DataFrame(rows)


def build_forecast_bundle(root: str | Path | None = None) -> ForecastBundle:
    metadata = load_phase_metadata(root)
    validation_metrics = load_validation_metrics(root)
    panel, panel_audit = load_panel(root)
    model_data, feature_audit = build_model_data(panel)
    forecast, selected_metrics, _train_seconds, selected_estimator = selected_forecast_frame(model_data)
    reference_metrics = evaluate_reference_forecasts(model_data[model_data["year"].eq(TEST_YEAR)], "test")
    test_summary = pd.concat([pd.DataFrame([selected_metrics]), reference_metrics], ignore_index=True)
    test_summary = test_summary.sort_values(["sMAPE_pct", "RMSE_MW"]).reset_index(drop=True)

    improvements = benchmark_improvements(selected_metrics, reference_metrics)
    monthly_error = grouped_error_summary(forecast, "month")
    hourly_error = grouped_error_summary(forecast, "hour")
    day_type_error = grouped_error_summary(forecast, "day_type")
    residual_summary = residual_diagnostics(forecast)

    return ForecastBundle(
        metadata=metadata,
        validation_metrics=validation_metrics,
        model_data=model_data,
        forecast_frame=forecast,
        selected_estimator=selected_estimator,
        test_summary=test_summary,
        selected_metrics=selected_metrics,
        benchmark_improvements=improvements,
        residual_summary=residual_summary,
        monthly_error=monthly_error,
        hourly_error=hourly_error,
        day_type_error=day_type_error,
        panel_audit=panel_audit,
        feature_audit=feature_audit,
    )


def _coerce_local_start(start_date, start_hour: int) -> pd.Timestamp:
    if not 0 <= int(start_hour) <= 23:
        raise ValueError("start_hour must be between 0 and 23")
    start_date_value = pd.Timestamp(start_date).date()
    start_naive = pd.Timestamp(pd.Timestamp.combine(start_date_value, datetime_time(hour=int(start_hour))))
    return start_naive.tz_localize(LOCAL_TZ, nonexistent="shift_forward", ambiguous=False)


def _scenario_demand_factor(timestamp: pd.Timestamp, settings: ScenarioSettings) -> float:
    years_after_test = max(0, int(timestamp.year) - TEST_YEAR)
    return max(0.2, 1.0 + years_after_test * float(settings.demand_growth_pct_per_year) / 100.0)


def _seasonal_profiles(model_data: pd.DataFrame) -> dict[str, pd.DataFrame | pd.Series]:
    source_columns = [TARGET, *WEATHER_DE_COLS, *RENEWABLE_LAG_SOURCE_COLS]
    missing_columns = [column for column in source_columns if column not in model_data.columns]
    if missing_columns:
        raise ValueError(f"Model data is missing scenario source columns: {missing_columns}")

    prepared = _ensure_calendar_columns(model_data)
    return {
        "month_weekday_hour": prepared.groupby(["month", "weekday_number", "hour"])[source_columns].median(),
        "month_hour": prepared.groupby(["month", "hour"])[source_columns].median(),
        "hour": prepared.groupby("hour")[source_columns].median(),
        "global": prepared[source_columns].median(numeric_only=True),
    }


def _profile_lookup(
    profiles: dict[str, pd.DataFrame | pd.Series],
    column: str,
    timestamp: pd.Timestamp,
) -> float:
    lookups = [
        ("month_weekday_hour", (timestamp.month, timestamp.weekday(), timestamp.hour)),
        ("month_hour", (timestamp.month, timestamp.hour)),
        ("hour", timestamp.hour),
    ]
    for profile_name, key in lookups:
        profile = profiles[profile_name]
        if key in profile.index:
            value = profile.loc[key, column]
            if pd.notna(value):
                return float(value)

    global_profile = profiles["global"]
    value = global_profile[column]
    if pd.notna(value):
        return float(value)
    raise ValueError(f"No historical seasonal profile value is available for {column}.")


def _scenario_source_value(
    profiles: dict[str, pd.DataFrame | pd.Series],
    column: str,
    timestamp: pd.Timestamp,
    settings: ScenarioSettings,
) -> float:
    value = _profile_lookup(profiles, column, timestamp)
    if column == "DE_temperature":
        return value + float(settings.temperature_shift_c)
    if column in RENEWABLE_LAG_SOURCE_COLS:
        return max(0.0, value * max(0.0, float(settings.renewable_generation_scale_pct)) / 100.0)
    return max(0.0, value)


def _scenario_load_seed(
    profiles: dict[str, pd.DataFrame | pd.Series],
    timestamp: pd.Timestamp,
    settings: ScenarioSettings,
) -> float:
    baseline = _profile_lookup(profiles, TARGET, timestamp)
    return max(0.0, baseline * _scenario_demand_factor(timestamp, settings))


def _calendar_feature_values(timestamp: pd.Timestamp) -> dict[str, float | int | pd.Timestamp]:
    weekday_number = timestamp.weekday()
    return {
        LOCAL_TIMESTAMP: timestamp,
        "year": timestamp.year,
        "month": timestamp.month,
        "weekday_number": weekday_number,
        "hour": timestamp.hour,
        "is_weekend": int(weekday_number >= 5),
        "day_type": "weekend" if weekday_number >= 5 else "weekday",
        "hour_sin": float(np.sin(2 * np.pi * timestamp.hour / 24)),
        "hour_cos": float(np.cos(2 * np.pi * timestamp.hour / 24)),
        "weekday_sin": float(np.sin(2 * np.pi * weekday_number / 7)),
        "weekday_cos": float(np.cos(2 * np.pi * weekday_number / 7)),
        "month_sin": float(np.sin(2 * np.pi * timestamp.month / 12)),
        "month_cos": float(np.cos(2 * np.pi * timestamp.month / 12)),
    }


def forecast_future_scenario(
    model_data: pd.DataFrame,
    estimator,
    *,
    start_date,
    start_hour: int,
    horizon_hours: int,
    settings: ScenarioSettings | None = None,
) -> pd.DataFrame:
    """Forecast future load from generated scenario inputs and recursive load lags."""
    if horizon_hours <= 0:
        raise ValueError("horizon_hours must be positive")

    scenario_settings = settings or ScenarioSettings()
    profiles = _seasonal_profiles(model_data)
    start_timestamp = _coerce_local_start(start_date, start_hour)
    forecast_index = pd.date_range(start=start_timestamp, periods=int(horizon_hours), freq="h")
    predicted_load_by_timestamp: dict[pd.Timestamp, float] = {}

    def load_for_lag(timestamp: pd.Timestamp) -> float:
        local_timestamp = pd.Timestamp(timestamp).tz_convert(LOCAL_TZ)
        return predicted_load_by_timestamp.get(
            local_timestamp,
            _scenario_load_seed(profiles, local_timestamp, scenario_settings),
        )

    rows = []
    for local_timestamp in forecast_index:
        local_timestamp = pd.Timestamp(local_timestamp).tz_convert(LOCAL_TZ)
        row = _calendar_feature_values(local_timestamp)
        row[JOIN_KEY] = local_timestamp.tz_convert("UTC")

        row["load_lag_1h"] = load_for_lag(local_timestamp - pd.Timedelta(hours=1))
        row["load_lag_24h"] = load_for_lag(local_timestamp - pd.Timedelta(hours=24))
        row["load_lag_168h"] = load_for_lag(local_timestamp - pd.Timedelta(hours=168))
        row["load_roll24_mean_lag1"] = float(
            np.mean([load_for_lag(local_timestamp - pd.Timedelta(hours=offset)) for offset in range(1, 25)])
        )
        row["load_roll168_mean_lag1"] = float(
            np.mean([load_for_lag(local_timestamp - pd.Timedelta(hours=offset)) for offset in range(1, 169)])
        )

        for source_column in [*WEATHER_DE_COLS, *RENEWABLE_LAG_SOURCE_COLS]:
            for lag in [1, 24]:
                source_timestamp = local_timestamp - pd.Timedelta(hours=lag)
                row[f"{source_column}_lag{lag}h"] = _scenario_source_value(
                    profiles,
                    source_column,
                    source_timestamp,
                    scenario_settings,
                )

        feature_frame = pd.DataFrame([row])
        prediction = float(np.asarray(estimator.predict(feature_frame[FULL_LAGGED_FEATURES]))[0])
        row["prediction_MW"] = max(0.0, prediction)
        row["scenario_demand_factor"] = _scenario_demand_factor(local_timestamp, scenario_settings)
        row["scenario_temperature_shift_C"] = float(scenario_settings.temperature_shift_c)
        row["scenario_renewable_generation_scale_pct"] = float(scenario_settings.renewable_generation_scale_pct)
        row["scenario_baseline_load_MW"] = _scenario_load_seed(profiles, local_timestamp, scenario_settings)
        rows.append(row)
        predicted_load_by_timestamp[local_timestamp] = row["prediction_MW"]

    return pd.DataFrame(rows)


def filter_forecast_frame(
    frame: pd.DataFrame,
    *,
    start_date,
    end_date,
    day_types: Iterable[str] | None = None,
) -> pd.DataFrame:
    filtered = frame.copy()
    local_dates = pd.to_datetime(filtered[LOCAL_TIMESTAMP]).dt.date
    mask = (local_dates >= start_date) & (local_dates <= end_date)
    if day_types:
        if "day_type" not in filtered.columns:
            filtered["day_type"] = np.where(filtered["is_weekend"].eq(1), "weekend", "weekday")
        mask &= filtered["day_type"].isin(list(day_types))
    return filtered.loc[mask].copy()


def select_forecast_window(
    frame: pd.DataFrame,
    *,
    start_date,
    start_hour: int,
    horizon_hours: int,
) -> pd.DataFrame:
    if horizon_hours <= 0:
        raise ValueError("horizon_hours must be positive")
    if not 0 <= start_hour <= 23:
        raise ValueError("start_hour must be between 0 and 23")

    prepared = frame.sort_values(LOCAL_TIMESTAMP).copy()
    start_naive = pd.Timestamp.combine(start_date, datetime_time(hour=start_hour))
    local_naive = pd.to_datetime(prepared[LOCAL_TIMESTAMP]).dt.tz_localize(None)
    return prepared.loc[local_naive >= start_naive].head(horizon_hours).copy()


def forecast_summary(frame: pd.DataFrame) -> dict[str, object]:
    if frame.empty:
        return {
            "rows": 0,
            "peak_forecast_MW": np.nan,
            "peak_timestamp": pd.NaT,
            "average_forecast_MW": np.nan,
            "minimum_forecast_MW": np.nan,
            "forecasted_energy_GWh": np.nan,
        }

    peak_index = frame["prediction_MW"].idxmax()
    return {
        "rows": int(len(frame)),
        "peak_forecast_MW": float(frame.loc[peak_index, "prediction_MW"]),
        "peak_timestamp": frame.loc[peak_index, LOCAL_TIMESTAMP],
        "average_forecast_MW": float(frame["prediction_MW"].mean()),
        "minimum_forecast_MW": float(frame["prediction_MW"].min()),
        "forecasted_energy_GWh": float(frame["prediction_MW"].sum() / 1_000),
    }


def aggregate_forecast_frame(frame: pd.DataFrame, frequency: str) -> pd.DataFrame:
    if frame.empty or frequency == "Hourly":
        return frame.sort_values(LOCAL_TIMESTAMP).copy()

    freq_map = {"Daily": "D", "Weekly": "W-MON"}
    if frequency not in freq_map:
        raise ValueError(f"Unsupported aggregation frequency: {frequency}")

    numeric_cols = [
        col
        for col in [TARGET, "prediction_MW", "load_lag_24h", "load_lag_168h", REFERENCE_FORECAST]
        if col in frame.columns
    ]
    aggregated = (
        frame.sort_values(LOCAL_TIMESTAMP)
        .set_index(LOCAL_TIMESTAMP)[numeric_cols]
        .resample(freq_map[frequency])
        .mean()
        .dropna(how="all")
        .reset_index()
    )
    if TARGET in aggregated.columns and "prediction_MW" in aggregated.columns:
        aggregated["residual_MW"] = aggregated[TARGET] - aggregated["prediction_MW"]
        aggregated["absolute_error_MW"] = aggregated["residual_MW"].abs()
        aggregated["absolute_sMAPE_pct"] = (
            2
            * aggregated["absolute_error_MW"]
            / (aggregated[TARGET].abs() + aggregated["prediction_MW"].abs())
            * 100
        )
    return aggregated


def metrics_for_prediction(frame: pd.DataFrame, prediction_col: str = "prediction_MW") -> dict[str, float | int]:
    valid = frame[[TARGET, prediction_col]].dropna()
    if valid.empty:
        return {"rows": 0, "sMAPE_pct": np.nan, "RMSE_MW": np.nan, "MAE_MW": np.nan, "R2": np.nan}
    return regression_metrics(valid[TARGET], valid[prediction_col], rows=len(valid))


def comparison_columns(selected_baselines: Iterable[str]) -> list[str]:
    columns = ["prediction_MW"]
    for label in selected_baselines:
        col = REFERENCE_PREDICTION_COLUMNS.get(label)
        if col and col not in columns:
            columns.append(col)
    return columns
