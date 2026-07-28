import unittest

import numpy as np
import pandas as pd

from src.energycast_core import (
    FULL_LAGGED_FEATURES,
    LOCAL_TIMESTAMP,
    REFERENCE_FORECAST,
    ScenarioSettings,
    TARGET,
    aggregate_forecast_frame,
    build_features,
    evaluate_reference_forecasts,
    filter_forecast_frame,
    forecast_future_scenario,
    forecast_summary,
    select_forecast_window,
    smape,
)


class DeterministicScenarioEstimator:
    def predict(self, frame):
        return (
            frame["load_lag_1h"].to_numpy(dtype=float) * 0.55
            + frame["load_lag_24h"].to_numpy(dtype=float) * 0.25
            + frame["DE_temperature_lag1h"].to_numpy(dtype=float) * 35.0
            + frame["DE_solar_generation_actual_lag1h"].to_numpy(dtype=float) * 0.04
            + frame["DE_wind_generation_actual_lag1h"].to_numpy(dtype=float) * 0.03
        )


class EnergyCastCoreTests(unittest.TestCase):
    def test_smape_uses_symmetric_percentage_and_ignores_zero_denominators(self):
        # Break caught: changing the denominator to actual-only MAPE or treating 0/0 as an error.
        actual = np.array([100.0, 200.0, 0.0])
        predicted = np.array([110.0, 180.0, 0.0])

        result = smape(actual, predicted)

        self.assertAlmostEqual(result, 10.0250626566)

    def test_build_features_uses_only_past_load_weather_and_renewable_values(self):
        # Break caught: using current-hour values in lag or rolling predictors.
        timestamps = pd.date_range("2019-01-01", periods=200, freq="h", tz="UTC")
        panel = pd.DataFrame(
            {
                "utc_timestamp": timestamps,
                LOCAL_TIMESTAMP: timestamps.tz_convert("Europe/Berlin"),
                TARGET: np.arange(200, dtype=float),
                REFERENCE_FORECAST: np.arange(200, dtype=float) + 1.0,
                "DE_temperature": np.arange(200, dtype=float) + 10.0,
                "DE_radiation_direct_horizontal": np.arange(200, dtype=float) + 20.0,
                "DE_radiation_diffuse_horizontal": np.arange(200, dtype=float) + 30.0,
                "DE_solar_generation_actual": np.arange(200, dtype=float) + 40.0,
                "DE_wind_generation_actual": np.arange(200, dtype=float) + 50.0,
                "year": [2019] * 200,
                "month": [1] * 200,
                "weekday_number": [1] * 200,
                "hour": [ts.hour for ts in timestamps.tz_convert("Europe/Berlin")],
                "is_weekend": [0] * 200,
            }
        )

        features = build_features(panel)
        row = features.iloc[168]

        self.assertEqual(row["load_lag_1h"], 167.0)
        self.assertEqual(row["load_lag_24h"], 144.0)
        self.assertEqual(row["load_lag_168h"], 0.0)
        self.assertEqual(row["DE_temperature_lag1h"], 177.0)
        self.assertEqual(row["DE_solar_generation_actual_lag24h"], 184.0)
        self.assertAlmostEqual(row["load_roll24_mean_lag1"], np.mean(np.arange(144.0, 168.0)))
        self.assertAlmostEqual(row["load_roll168_mean_lag1"], np.mean(np.arange(0.0, 168.0)))

    def test_reference_forecasts_report_metrics_and_drop_missing_reference_rows(self):
        # Break caught: evaluating ENTSO-E rows with missing predictions instead of dropping them.
        frame = pd.DataFrame(
            {
                TARGET: [100.0, 110.0, 120.0],
                "load_lag_24h": [90.0, 100.0, 110.0],
                "load_lag_168h": [95.0, 105.0, 115.0],
                REFERENCE_FORECAST: [98.0, np.nan, 119.0],
            }
        )

        metrics = evaluate_reference_forecasts(frame, split_name="test")
        entsoe = metrics.loc[metrics["candidate"].eq("ENTSO-E day-ahead forecast")].iloc[0]
        naive = metrics.loc[metrics["candidate"].eq("24h naive persistence")].iloc[0]

        self.assertEqual(entsoe["rows"], 2)
        self.assertEqual(naive["rows"], 3)
        self.assertLess(entsoe["sMAPE_pct"], naive["sMAPE_pct"])

    def test_filter_and_aggregate_forecast_frame_respect_date_and_day_type(self):
        # Break caught: controls applying only visually while metrics still use the unfiltered data.
        frame = pd.DataFrame(
            {
                LOCAL_TIMESTAMP: pd.to_datetime(
                    [
                        "2019-01-01 00:00",
                        "2019-01-01 01:00",
                        "2019-01-02 00:00",
                    ],
                    utc=True,
                ),
                "day_type": ["weekday", "weekday", "weekend"],
                TARGET: [100.0, 120.0, 90.0],
                "prediction_MW": [110.0, 100.0, 95.0],
                "load_lag_24h": [90.0, 115.0, 85.0],
            }
        )

        filtered = filter_forecast_frame(
            frame,
            start_date=pd.Timestamp("2019-01-01").date(),
            end_date=pd.Timestamp("2019-01-01").date(),
            day_types=["weekday"],
        )
        aggregated = aggregate_forecast_frame(filtered, frequency="Daily")

        self.assertEqual(len(filtered), 2)
        self.assertEqual(len(aggregated), 1)
        self.assertEqual(aggregated.iloc[0][TARGET], 110.0)
        self.assertEqual(aggregated.iloc[0]["prediction_MW"], 105.0)

    def test_select_forecast_window_and_summary_drive_forecast_kpis(self):
        # Break caught: forecast controls selecting a visual slice while KPIs come from a different window.
        frame = pd.DataFrame(
            {
                LOCAL_TIMESTAMP: pd.date_range("2019-01-01 00:00", periods=4, freq="h", tz="Europe/Berlin"),
                "prediction_MW": [100.0, 120.0, 90.0, 110.0],
                TARGET: [101.0, 119.0, 91.0, 112.0],
            }
        )

        window = select_forecast_window(
            frame,
            start_date=pd.Timestamp("2019-01-01").date(),
            start_hour=1,
            horizon_hours=2,
        )
        summary = forecast_summary(window)

        self.assertEqual(list(window["prediction_MW"]), [120.0, 90.0])
        self.assertEqual(summary["peak_forecast_MW"], 120.0)
        self.assertEqual(summary["peak_timestamp"], pd.Timestamp("2019-01-01 01:00", tz="Europe/Berlin"))
        self.assertEqual(summary["average_forecast_MW"], 105.0)
        self.assertEqual(summary["forecasted_energy_GWh"], 0.21)

    def test_future_scenario_forecast_generates_model_features_without_actual_target(self):
        # Break caught: future forecast replaying 2019 rows instead of creating future model inputs.
        model_data = self._scenario_model_data()

        forecast = forecast_future_scenario(
            model_data,
            DeterministicScenarioEstimator(),
            start_date=pd.Timestamp("2026-07-28").date(),
            start_hour=6,
            horizon_hours=48,
            settings=ScenarioSettings(
                demand_growth_pct_per_year=1.0,
                temperature_shift_c=0.5,
                renewable_generation_scale_pct=110.0,
            ),
        )

        self.assertEqual(len(forecast), 48)
        self.assertEqual(forecast[LOCAL_TIMESTAMP].iloc[0], pd.Timestamp("2026-07-28 06:00", tz="Europe/Berlin"))
        self.assertTrue(forecast["prediction_MW"].notna().all())
        self.assertNotIn(TARGET, forecast.columns)
        for column in FULL_LAGGED_FEATURES:
            self.assertIn(column, forecast.columns)
            self.assertTrue(forecast[column].notna().all())

    def test_future_scenario_controls_change_forecast_path(self):
        # Break caught: scenario sliders that do not actually affect the model feature rows.
        model_data = self._scenario_model_data()
        estimator = DeterministicScenarioEstimator()

        reference = forecast_future_scenario(
            model_data,
            estimator,
            start_date=pd.Timestamp("2026-01-15").date(),
            start_hour=0,
            horizon_hours=24,
            settings=ScenarioSettings(),
        )
        warmer_higher_growth = forecast_future_scenario(
            model_data,
            estimator,
            start_date=pd.Timestamp("2026-01-15").date(),
            start_hour=0,
            horizon_hours=24,
            settings=ScenarioSettings(
                demand_growth_pct_per_year=3.0,
                temperature_shift_c=2.0,
                renewable_generation_scale_pct=125.0,
            ),
        )

        self.assertFalse(np.allclose(reference["prediction_MW"], warmer_higher_growth["prediction_MW"]))

    def _scenario_model_data(self):
        timestamps = pd.date_range("2015-01-01 00:00", periods=24 * 420, freq="h", tz="Europe/Berlin")
        hours = np.arange(len(timestamps), dtype=float)
        panel = pd.DataFrame(
            {
                "utc_timestamp": timestamps.tz_convert("UTC"),
                LOCAL_TIMESTAMP: timestamps,
                TARGET: 52_000
                + 4_000 * np.sin(2 * np.pi * timestamps.hour / 24)
                + 1_200 * np.cos(2 * np.pi * timestamps.dayofyear / 365)
                + hours * 0.2,
                REFERENCE_FORECAST: 52_500,
                "DE_temperature": 8 + 12 * np.sin(2 * np.pi * timestamps.dayofyear / 365),
                "DE_radiation_direct_horizontal": np.maximum(0, 400 * np.sin(2 * np.pi * (timestamps.hour - 6) / 24)),
                "DE_radiation_diffuse_horizontal": np.maximum(0, 150 * np.sin(2 * np.pi * (timestamps.hour - 5) / 24)),
                "DE_solar_generation_actual": np.maximum(0, 18_000 * np.sin(2 * np.pi * (timestamps.hour - 6) / 24)),
                "DE_wind_generation_actual": 15_000 + 2_000 * np.cos(2 * np.pi * timestamps.dayofyear / 20),
                "year": timestamps.year,
                "month": timestamps.month,
                "weekday_number": timestamps.weekday,
                "hour": timestamps.hour,
                "is_weekend": (timestamps.weekday >= 5).astype(int),
            }
        )
        features = build_features(panel)
        model_data = features.dropna(subset=[TARGET, "load_lag_1h", "load_lag_24h", "load_lag_168h"]).copy()
        model_data["day_type"] = np.where(model_data["is_weekend"].eq(1), "weekend", "weekday")
        return model_data


if __name__ == "__main__":
    unittest.main()
