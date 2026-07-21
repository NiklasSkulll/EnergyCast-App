# ⚡EnergyCast-App

[![Python](https://img.shields.io/badge/Python-3.11-%231D9FD7?style=plastic&logo=python&logoColor=%23FF6600)](pyproject.toml)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-%23F37626?style=plastic&logo=jupyter&logoColor=%23FF6600)](https://jupyter.org/)
[![uv](https://img.shields.io/badge/uv-Environment%20Manager-%23DE5FE9?style=plastic&logo=uv&logoColor=%23FF6600)](uv.lock)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-%237A76FF?style=plastic&logo=plotly&logoColor=%23FF6600)](https://plotly.com/python/)
[![GitLFS](https://img.shields.io/badge/Git%20LFS-Storing%20large%20Files-%23F64935?style=plastic&logo=gitlfs&logoColor=%23FF6600)](https://git-lfs.com/)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-%23FFFF66?style=plastic&logo=opensourceinitiative&logoColor=%23FF6600)](LICENSE)

---

Smart-grid load forecasting for Germany (2015-2019) using weather, renewable generation, calendar effects, and historical demand. This repository follows the QUA3CK process model (Question, Understanding, Algorithms, Conclude, Knowledge transfer) and is structured around phase notebooks.

## Project goals

- Forecast hourly electricity load in Germany using time-series and exogenous features.
- Evaluate multiple models and feature sets using time-aware splits.
- Provide a reproducible workflow and documentation for sustainable energy planning.

## Data

**Raw data lives in data/raw:**
- data/raw/time_series_60min_singleindex.csv
- data/raw/weather_data.csv

Processed and interim datasets should go to data/processed and data/interim.

**Data sources (Open Power System Data):**
- Time series: https://data.open-power-system-data.org/time_series/2020-10-06
- Weather data: https://data.open-power-system-data.org/weather_data/latest/

## Folder structure

```text
EnergyCast-App/
├─ .serena/                 # Serena project config, cache, and memories
├─ app/                     # Placeholder for a future app or dashboard
├─ data/
│  ├─ raw/                  # Original datasets
│  │  ├─ time_series_60min_singleindex.csv
│  │  └─ weather_data.csv
│  ├─ interim/              # Intermediate processing outputs
│  └─ processed/            # Cleaned and feature-engineered data
├─ docs/                    # Project docs and methodology notes
├─ models/                  # Trained models and artifacts
├─ notebooks/               # QUA3CK phase notebooks
├─ src/                     # Reusable Python modules
├─ LICENSE
├─ README.md
└─ pyproject.toml
```

## Setup (uv)

Use uv for environment and dependency management:

```bash
uv venv
uv sync
uv run jupyter lab
```

Select the .venv kernel when prompted in Jupyter.

## Usage

Run the notebooks in order:

1. notebooks/01_Q_Phase.ipynb
2. notebooks/02_U_Phase.ipynb
3. notebooks/03_A_Phase.ipynb
4. notebooks/04_C_Phase.ipynb
5. notebooks/05_K_Phase.ipynb

## Modeling approach

- Target: hourly electricity load in Germany.
- Features: weather (temperature, solar radiation), renewables (wind/solar generation), calendar effects, and lagged load features.
- Metrics: MAE, RMSE, sMAPE, and R2.
- Splits: time-based (train 2015-2017, validate 2018, test 2019).

## Documentation

- Project plan: [docs/Project_plan_and_structure.md](docs/Project_plan_and_structure.md)
- QUA3CK overview: [docs/QUACK_process_model.md](docs/QUACK_process_model.md)
- DIG framework notes: [docs/DIG_framework.md](docs/DIG_framework.md)
- Serena setup: [docs/Serena_setup.md](docs/Serena_setup.md)

## Tooling

- Serena is configured in .serena/project.yml for indexing and symbol navigation.

## Contributing

- Keep functions small and reusable.
- Add notebook references where code is used.
- Do not write to data/ unless explicitly requested.

## License

MIT License. See [LICENSE](LICENSE).
