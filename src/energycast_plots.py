from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.energycast_core import LOCAL_TIMESTAMP, REFERENCE_FORECAST, TARGET

SERIES_LABELS = {
    TARGET: "Actual load",
    "prediction_MW": "Selected model",
    "load_lag_24h": "24h naive",
    "load_lag_168h": "168h naive",
    REFERENCE_FORECAST: "ENTSO-E forecast",
}

SERIES_COLORS = {
    TARGET: "#222222",
    "prediction_MW": "#007C89",
    "load_lag_24h": "#D95F02",
    "load_lag_168h": "#6A3D9A",
    REFERENCE_FORECAST: "#1F78B4",
}


def make_test_comparison_figure(metrics: pd.DataFrame) -> go.Figure:
    plot_data = metrics.copy()
    fig = px.bar(
        plot_data,
        x="candidate",
        y="sMAPE_pct",
        color="candidate_type",
        color_discrete_sequence=["#007C89", "#D95F02", "#6A3D9A", "#1F78B4"],
        labels={"candidate": "", "sMAPE_pct": "sMAPE (%)", "candidate_type": "Candidate type"},
        title="Held-out 2019 sMAPE comparison",
    )
    fig.add_hline(y=5.0, line_dash="dash", line_color="#444444", annotation_text="Q-phase threshold")
    fig.update_layout(xaxis_tickangle=-25, legend_orientation="h", legend_y=-0.35, margin=dict(l=20, r=20, t=60, b=120))
    return fig


def make_validation_figure(validation_metrics: pd.DataFrame) -> go.Figure:
    plot_data = validation_metrics.sort_values("sMAPE_pct", ascending=True).copy()
    fig = px.bar(
        plot_data,
        x="sMAPE_pct",
        y="model",
        orientation="h",
        color="feature_set",
        color_discrete_sequence=["#007C89", "#E6AB02", "#7570B3"],
        labels={"sMAPE_pct": "2018 validation sMAPE (%)", "model": "", "feature_set": "Feature set"},
        title="A-phase validation ranking",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=60, b=20))
    return fig


def make_forecast_figure(frame: pd.DataFrame, prediction_columns: list[str]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=frame[LOCAL_TIMESTAMP],
            y=frame[TARGET],
            mode="lines",
            name=SERIES_LABELS[TARGET],
            line=dict(color=SERIES_COLORS[TARGET], width=2),
        )
    )
    for column in prediction_columns:
        if column not in frame.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=frame[LOCAL_TIMESTAMP],
                y=frame[column],
                mode="lines",
                name=SERIES_LABELS.get(column, column),
                line=dict(color=SERIES_COLORS.get(column, "#666666"), width=2, dash="solid" if column == "prediction_MW" else "dot"),
            )
        )
    fig.update_layout(
        title="Actual load and forecast comparison",
        xaxis_title="Local timestamp",
        yaxis_title="Load (MW)",
        hovermode="x unified",
        legend_orientation="h",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def make_forecast_output_figure(frame: pd.DataFrame, *, show_actual: bool = False) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=frame[LOCAL_TIMESTAMP],
            y=frame["prediction_MW"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color=SERIES_COLORS["prediction_MW"], width=3),
        )
    )
    if show_actual and TARGET in frame.columns:
        fig.add_trace(
            go.Scatter(
                x=frame[LOCAL_TIMESTAMP],
                y=frame[TARGET],
                mode="lines",
                name="Historical actual",
                line=dict(color=SERIES_COLORS[TARGET], width=2, dash="dot"),
            )
        )
    fig.update_layout(
        title="Forecasted electricity load",
        xaxis_title="Local timestamp",
        yaxis_title="Load (MW)",
        hovermode="x unified",
        legend_orientation="h",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def make_input_context_figure(frame: pd.DataFrame) -> go.Figure:
    context_columns = [
        "load_lag_1h",
        "load_lag_24h",
        "load_lag_168h",
        "load_roll24_mean_lag1",
    ]
    fig = go.Figure()
    for column in context_columns:
        if column not in frame.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=frame[LOCAL_TIMESTAMP],
                y=frame[column],
                mode="lines",
                name=SERIES_LABELS.get(column, column.replace("_", " ")),
            )
        )
    fig.update_layout(
        title="Recent-load inputs used by the forecast",
        xaxis_title="Forecast timestamp",
        yaxis_title="Load feature (MW)",
        hovermode="x unified",
        legend_orientation="h",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def make_residual_figure(frame: pd.DataFrame, threshold_mw: int) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=frame[LOCAL_TIMESTAMP],
            y=frame["residual_MW"],
            mode="lines",
            name="Residual",
            line=dict(color="#007C89", width=1.5),
        )
    )
    fig.add_hline(y=0, line_color="#444444", line_width=1)
    fig.add_hline(y=threshold_mw, line_dash="dash", line_color="#D95F02")
    fig.add_hline(y=-threshold_mw, line_dash="dash", line_color="#D95F02")
    fig.update_layout(
        title="Residuals: actual minus prediction",
        xaxis_title="Local timestamp",
        yaxis_title="Residual (MW)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def make_monthly_error_figure(monthly_error: pd.DataFrame) -> go.Figure:
    plot_data = monthly_error.sort_values("month").copy()
    fig = px.bar(
        plot_data,
        x="month",
        y="sMAPE_pct",
        color="MAE_MW",
        color_continuous_scale=["#B2DF8A", "#FDBF6F", "#E31A1C"],
        labels={"month": "Month", "sMAPE_pct": "sMAPE (%)", "MAE_MW": "MAE (MW)"},
        title="Monthly selected-model error",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig


def make_hourly_error_figure(hourly_error: pd.DataFrame) -> go.Figure:
    plot_data = hourly_error.sort_values("hour").copy()
    fig = px.bar(
        plot_data,
        x="hour",
        y="sMAPE_pct",
        color="bias_MW",
        color_continuous_scale="RdBu",
        labels={"hour": "Hour of day", "sMAPE_pct": "sMAPE (%)", "bias_MW": "Bias (MW)"},
        title="Hour-of-day error pattern",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig
