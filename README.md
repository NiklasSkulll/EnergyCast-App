# EnergyCast-App

Smart-grid load forecasting for Germany (2015-2019) using weather, renewable generation, calendar effects, and historical demand. This repository follows the QUA3CK process model (Question, Understanding, Algorithms, Conclude, Knowledge transfer) and is structured around notebook phases.

## Project goals

- Forecast hourly electricity load in Germany using time-series and exogenous features.
- Evaluate multiple models and feature sets using time-aware splits.
- Provide a reproducible workflow and documentation for sustainable energy planning.

## Data

Raw data lives in data/raw:

- data/raw/time_series_60min_singleindex.csv (https://data.open-power-system-data.org/time_series/2020-10-06)
- data/raw/weather_data.csv (https://data.open-power-system-data.org/weather_data/latest/)

Processed and interim datasets should go to data/processed and data/interim.

Data sources are based on Open Power System Data (OPSD) time series and weather data (see docs for details).

## Repository structure

- app: placeholder for a future app or dashboard
- data: raw, interim, and processed datasets
- docs: project plan and QUA3CK process description
- models: trained models and artifacts
- notebooks: QUA3CK phase notebooks
- src: reusable code (currently empty)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If requirements.txt is still empty, add the packages you use in notebooks (typical: pandas, numpy, scikit-learn, matplotlib, seaborn).

## Usage

Run the notebooks in order:

1. notebooks/01_Q_Phase.ipynb
2. notebooks/02_U_Phase.ipynb
3. notebooks/03_A_Phase.ipynb
4. notebooks/04_C_Phase.ipynb
5. notebooks/05_K_Phase.ipynb

```bash
jupyter lab
```

## Modeling approach

- Target: hourly electricity load in Germany.
- Features: weather (temperature, solar radiation), renewables (wind/solar generation), calendar effects, and lagged load features.
- Metrics: MAE, RMSE, sMAPE, and R2.
- Splits: time-based (e.g., train 2015-2017, validate 2018, test 2019).

## Documentation

- Project plan: [docs/Project_plan_and_structure.md](docs/Project_plan_and_structure.md)
- QUA3CK overview: [docs/QUACK_process_model.md](docs/QUACK_process_model.md)

## Contributing

If you add code to src, keep functions small and reusable, and add notebook references where they are used.

## License

No license file is present. Add one if you plan to distribute this project.
