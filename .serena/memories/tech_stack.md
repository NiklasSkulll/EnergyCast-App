# Tech Stack

- Python project managed by `uv`; `pyproject.toml` has `[tool.uv] package = false` and no installable package metadata beyond project deps.
- Python version constraint: `>=3.11,<3.12`. No `.python-version` file is present.
- Core dependencies: pandas, numpy, scipy, statsmodels, plotly, jupyter, ipykernel, scikit-learn, xgboost, streamlit.
- Testing uses stdlib `unittest`; Streamlit smoke/UI assertions use `streamlit.testing.v1.AppTest`.
- No configured ruff/black/isort/mypy/pytest sections in `pyproject.toml` at onboarding time.
- Plotly is the expected charting library for notebooks/app visuals unless user requests otherwise.
- Large raw CSVs are Git LFS objects; setup docs expect `git lfs pull` after clone.