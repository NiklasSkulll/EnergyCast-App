# AGENTS Guide (EnergyCast-App)

## Purpose

This repository follows the QUA3CK process model using phase notebooks. Agents should keep work aligned to the current phase and avoid jumping ahead without approval.

## Project context

- Goal: Forecast hourly electricity load in Germany (2015-2019) using weather, renewables, calendar effects, and historical load.
- Data: Raw files live in data/raw. Intermediate outputs belong in data/interim or data/processed only when explicitly requested.
- Workflow: One notebook per QUA3CK phase in notebooks/.

## Environment and tooling

- Use uv for Python environment management.
- Prefer running notebooks with uv (uv run jupyter lab) and the .venv kernel.
- Keep dependencies minimal and justified.

## Notebook guidelines

- Keep notebooks readable: brief markdown before and after analysis blocks.
- Use pathlib for file paths and ensure notebooks run from repo root.
- Favor reusable helper functions for repeated logic.
- Use Plotly for charts unless requested otherwise.
- Do not write to data/ unless explicitly requested; default to read-only.

## Data handling

- Do not modify raw datasets in data/raw.
- Always document missingness, duplicates, and time coverage in Phase U.
- For Germany-focused analysis, prefer DE_ columns and document why.

## Coding standards

- Keep functions small and single-purpose.
- Use explicit variable names for targets and join keys.
- Add brief comments only for non-obvious logic.

## Outputs by phase

- Q: Research question, KPIs, scope, and evaluation design.
- U: Data understanding, quality issues, and readiness for modeling.
- A3: Feature engineering, model selection, and tuning.
- C: Model comparison and selection.
- K: Knowledge transfer and documentation artifacts.

## Safety and reproducibility

- Avoid destructive commands unless explicitly requested.
- Preserve existing user changes unless asked to revert.
- Keep outputs deterministic where possible (fixed random seeds).
