<div align="center">

# ⚡EnergyCast-App

[![Python](https://img.shields.io/badge/Python-3.11-%231D9FD7?style=plastic&logo=python&logoColor=%231D9FD7&labelColor=%23282C33)](pyproject.toml)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-%23F37626?style=plastic&logo=jupyter&logoColor=%23F37626&labelColor=%23282C33)](https://jupyter.org/)
[![uv](https://img.shields.io/badge/uv-Environment%20Manager-%23DE5FE9?style=plastic&logo=uv&logoColor=%23DE5FE9&labelColor=%23282C33)](uv.lock)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-%23FF4B4B?style=plastic&logo=streamlit&logoColor=%23FF4B4B&labelColor=%23282C33)](app/streamlit_app.py)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-%237A76FF?style=plastic&logo=plotly&logoColor=%237A76FF&labelColor=%23282C33)](https://plotly.com/python/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-%23F7931E?style=plastic&logo=scikitlearn&logoColor=%23F7931E&labelColor=%23282C33)](https://scikit-learn.org/)
[![GitLFS](https://img.shields.io/badge/Git%20LFS-Large%20Files-%23F64935?style=plastic&logo=gitlfs&logoColor=%23F64935&labelColor=%23282C33)](https://git-lfs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-%23FFFF66?style=plastic&logo=opensourceinitiative&logoColor=%23FFFF66&labelColor=%23282C33)](LICENSE)

**EnergyCast** forecasts Germany's national hourly electricity load. The project follows the QUA³CK process model and contains the full path from research question to data understanding, model training, validation and a Streamlit scenario forecast app.

The selected model is a `HistGradientBoostingRegressor` trained on 2015-2018 OPSD data and validated on the unseen 2019 holdout year. The Streamlit app is not a model-statistics dashboard: it uses the trained model to forecast future hourly load from generated scenario inputs.

**Streamlit scenario forecast app:** [https://energycast-app.streamlit.app/](https://energycast-app.streamlit.app/)

</div>

---

## Table of Contents

- [Current Result](#current-result)
- [How the Forecast works](#how-the-forecast-works)
- [Repository Structure](#repository-structure)
- [Data](#data)
- [First-time Setup](#first-time-setup)
    - [1. Install uv](#1-install-uv)
    - [2. Install Git LFS before cloning](#2-install-git-lfs-before-cloning)
    - [3. Clone and pull LFS Objects](#3-clone-and-pull-lfs-objects)
    - [4. Create the Python Environment](#4-create-the-python-environment)
- [Run the App locally](#run-the-app-locally)
    - [Start the App](#start-the-app)
    - [Stop the App](#stop-the-app)
- [Run the Notebooks](#run-the-notebooks)
- [Run Tests](#run-tests)
- [Important Files](#important-files)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Current Result

- **Target:** `DE_load_actual_entsoe_transparency` in MW.
- **Selected model:** `HistGradientBoosting regressor - full lagged feature set`.
- **Training/validation years:** 2015-2018.
- **Final holdout test year:** 2019.
- **2019 holdout performance:** about `0.757%` sMAPE and `412.9 MW` MAE.
- **App scope:** scenario forecasts for future timestamps, currently 2020-2030.

---

## How the Forecast works

The model needs feature rows before it can forecast. During validation, those feature rows come from historical data. For future timestamps, the app generates the required inputs first and then calls the trained model.

**Future app inputs are generated from:**
- calendar features such as hour, weekday, month and weekend flag.
- historical seasonal load profiles.
- generated lagged weather and renewable-generation inputs.
- user scenario controls for demand growth, temperature shift, and renewable generation scale.
- recursive load lags, where earlier forecasted load values become later lag inputs.

This means 2020+ outputs are scenario forecasts, not measured future truth. A production system would replace generated assumptions with live load history plus real weather and renewable forecasts available at prediction time.

---

## Repository Structure

```text
EnergyCast-App/
├─ app/
│  └─ streamlit_app.py              # Scenario forecast app
├─ data/
│  ├─ raw/                          # Git LFS raw OPSD data
│  ├─ interim/                      # Intermediate outputs
│  └─ processed/                    # A-phase metrics/training summaries
├─ docs/
│  ├─ course-material/              # Course context
│  ├─ data-set-information/         # Dataset field docs
│  ├─ project-plan-and-frameworks/  # QUA³CK/DIG/project docs
│  ├─ prompts/                      # Phase prompts
│  └─ setup-instructions/           # Extra setup notes
├─ models/                          # Selected model artifact and metadata
├─ notebooks/                       # QUA³CK phase notebooks
├─ src/                             # Reusable forecast and plotting code
├─ tests/                           # Core and Streamlit tests
├─ pyproject.toml
└─ uv.lock
```

---

## Data

**Raw data is stored with Git LFS:**
- `data/raw/time_series_60min_singleindex.csv`
- `data/raw/weather_data.csv`

**Sources:**
- **OPSD time series:** [https://data.open-power-system-data.org/time_series/2020-10-06](https://data.open-power-system-data.org/time_series/2020-10-06)
- **OPSD weather data:** [https://data.open-power-system-data.org/weather_data/latest/](https://data.open-power-system-data.org/weather_data/latest/)
- view [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md) for more informations.

---

## First-time Setup

### 1. Install uv

**Official uv installation docs:** [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

**Linux/WSL:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**After installation, restart the terminal if needed and check:**
```bash
uv --version
```

### 2. Install Git LFS before cloning

**Official Git LFS site:** [https://git-lfs.com/](https://git-lfs.com/)

**Linux/WSL:**
```bash
sudo apt update
sudo apt install git-lfs
git lfs install
```

`git lfs install` only needs to be run once per user account.

### 3. Clone and pull LFS Objects

**Linux/WSL:**
```bash
git clone <repo-url>
cd EnergyCast-App
git lfs pull
git lfs ls-files
```

**Validation:**
> If the raw CSV files look tiny or contain text beginning with `version https://git-lfs.github.com/spec/v1`, the real LFS objects were not downloaded. **Run:** `git lfs pull`

### 4. Create the Python Environment

**From the repository root:**
```bash
uv sync
```

`uv sync` creates/updates `.venv` from `pyproject.toml` and `uv.lock`.

---

## Run the App locally

### Start the App

**From the repository root, use:**
```bash
uv run streamlit run app/streamlit_app.py
```

Streamlit prints a local URL, usually: `http://localhost:8501`

> If you want to force the same local address used during development, use `uv run streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501`

### Stop the App

**To stop the app, click into the terminal where Streamlit is running and press:**
```text
Ctrl+C
```

> If port `8501` is already in use, either stop the older Streamlit run with `Ctrl+C` or start on another port: `uv run streamlit run app/streamlit_app.py --server.port 8502`

The `Deploy` button in the top-right corner is Streamlit's built-in toolbar. It is not part of the EnergyCast app and does not mean the local app is publicly deployed.

---

## Run the Notebooks

**Start Jupyter:**
```bash
uv run jupyter lab
```

**Use the `.venv` kernel and run the notebooks in order:**
1. `notebooks/001_Q_Phase.ipynb`
2. `notebooks/002_U_Phase.ipynb`
3. `notebooks/003_A_Phase.ipynb`
4. `notebooks/004_C_Phase.ipynb`
5. `notebooks/005_K_Phase.ipynb`

**To execute the K-phase notebook from the terminal:**
```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/005_K_Phase.ipynb
```

---

## Run Tests

```bash
uv run python -m unittest discover -s tests -v
```

**The tests cover:**
- leakage-safe lag feature creation.
- metric calculations and reference forecast evaluation.
- future scenario feature generation.
- Streamlit rendering and app structure.

---

## Important Files

- **`app/streamlit_app.py`:** Streamlit scenario forecast app.
- **`src/energycast_core.py`:** data loading, feature engineering, model fitting, validation metrics, future scenario generation.
- **`src/energycast_plots.py`:** Plotly chart builders.
- **`models/003_A_Phase_candidate_model_metadata.json`:** selected model metadata and feature list.
- **`notebooks/005_K_Phase.ipynb`:** knowledge-transfer notebook for the app.
- **`docs/setup-instructions/Git_LFS_Setup.md`:** extra Git LFS notes.

---

## Troubleshooting

- **`uv: command not found`:** restart the terminal, then check `uv --version`.
- **Missing raw data or tiny CSV files:** run `git lfs install` and `git lfs pull`.
- **Streamlit port conflict:** stop the old run with `Ctrl+C` or use e.g. `--server.port 8502`.
- **Slow first app load:** the app builds the data/model bundle once and then caches it.

## License

MIT License. See [LICENSE](LICENSE).
