# A3 Phase Checkpoint Logging GPU Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reproducible checkpointing, progress logging, and safe optional GPU-aware model support to `notebooks/003_A_Phase.ipynb` without moving the notebook beyond A3 scope.

**Architecture:** Keep the new helpers inside the notebook because this repository is notebook-first, `src/` only contains `.gitkeep`, and `pyproject.toml` has `package = false`. The notebook will create predictable directories, configure a dual notebook/file logger, save and validate per-model checkpoints, include XGBoost as the GPU-capable candidate from the uv-managed environment, and save A-phase handoff artifacts without using the reserved 2019 test data for model selection.

**Tech Stack:** Python 3.11, pathlib, logging, joblib from the existing lockfile, pandas, NumPy, scikit-learn, Plotly, XGBoost 2.x or newer with safe CPU/GPU device resolution.

---

## Existing Context

- `notebooks/003_A_Phase.ipynb` currently has no checkpointing, no logging, no `data/processed` writes, no `logs` writes, and no GPU-related code.
- `data/processed/checkpoints/`, `logs/`, and `models/` already exist as repository directories, but only `.gitkeep` files are present.
- `src/` exists but has no reusable project modules. Keep helper functions in the notebook to avoid creating a package import path just for this notebook.
- The A notebook uses a classification adaptation of the original load-forecasting project. It trains `DummyClassifier`, `LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier`, `KNeighborsClassifier`, and `LinearSVC` with `TimeSeriesSplit`.
- The course material frames A3 as iterative algorithm selection, feature adaptation, and hyperparameter adjustment. It also emphasizes reproducibility through parameters, metrics, model versions, artifacts, and experiment runs.
- The current notebook correctly keeps 2019 as a reserved test year for C phase. Preserve that boundary.
- New user requirement: add XGBoost to the uv-managed project dependencies for GPU-capable model support.

## Files

- Modify: `notebooks/003_A_Phase.ipynb`
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- `joblib` is already present in `uv.lock` through scikit-learn. XGBoost is added through `uv add "xgboost>=2.0"` so GPU-capable support is reproducible from a clean `uv sync`.
- Generated when the notebook runs:
  - `logs/<YYYY-MM-DD>_A_Phase.log`
  - `data/processed/checkpoints/003_A_Phase__<model_slug>.joblib`
  - `data/processed/checkpoints/003_A_Phase__<model_slug>.metadata.json`
  - `data/processed/003_A_Phase_training_summary.csv`
  - `data/processed/003_A_Phase_validation_metrics.csv`
  - `models/003_A_Phase_candidate_model.joblib`
  - `models/003_A_Phase_candidate_model_metadata.json`

---

### Task 1: Add Setup Imports, Directories, Logging, and GPU Resolution

**Files:**
- Modify: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Replace the first import code cell with this exact source**

```python
from datetime import date, datetime, timezone
import importlib
import importlib.util
import json
import logging
from pathlib import Path
import re
import subprocess
import sys
import time
import warnings

from IPython.display import display
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sklearn

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore", category=ConvergenceWarning)

pd.set_option("display.max_columns", 120)
pd.set_option("display.width", 160)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
```

- [ ] **Step 2: Replace the project constants code cell with this exact source**

```python
ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
CHECKPOINT_DIR = PROCESSED_DIR / "checkpoints"
LOG_DIR = ROOT / "logs"
MODEL_DIR = ROOT / "models"

for directory in [PROCESSED_DIR, CHECKPOINT_DIR, LOG_DIR, MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

TIME_SERIES_PATH = RAW_DIR / "time_series_60min_singleindex.csv"
WEATHER_PATH = RAW_DIR / "weather_data.csv"

JOIN_KEY = "utc_timestamp"
SOURCE_LOCAL_TIMESTAMP_COL = "cet_cest_timestamp"
LOCAL_TIMESTAMP = "local_timestamp"
LOCAL_TZ = "Europe/Berlin"

TARGET = "DE_load_actual_entsoe_transparency"
HIGH_LOAD_LABEL = "high_load"
HIGH_LOAD_QUANTILE = 0.75
EXPECTED_HIGH_LOAD_THRESHOLD_MW = 64_472.5

Q_START_YEAR = 2015
Q_END_YEAR = 2019
EXPECTED_Q_ROWS = 43_824

TRAIN_YEARS = range(2015, 2018)
VALIDATION_YEAR = 2018
RESERVED_TEST_YEAR = 2019
EXPECTED_MODEL_ROWS = 43_655
EXPECTED_SPLIT_ROWS = {"train": 26_135, "validation": 8_760, "reserved_test": 8_760}

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
    *RENEWABLE_LAG_SOURCE_COLS,
]
WEATHER_SELECTED_COLS = [JOIN_KEY, *WEATHER_DE_COLS]

A_PHASE_TRAINING_SUMMARY_PATH = PROCESSED_DIR / "003_A_Phase_training_summary.csv"
A_PHASE_VALIDATION_METRICS_PATH = PROCESSED_DIR / "003_A_Phase_validation_metrics.csv"
A_PHASE_MODEL_PATH = MODEL_DIR / "003_A_Phase_candidate_model.joblib"
A_PHASE_MODEL_METADATA_PATH = MODEL_DIR / "003_A_Phase_candidate_model_metadata.json"

for path in [TIME_SERIES_PATH, WEATHER_PATH]:
    assert path.exists(), f"Missing required raw file: {path}"
```

- [ ] **Step 3: Insert this markdown cell immediately after the project constants code cell**

```markdown
## Reproducibility utilities

The following utilities support the iterative A3 workflow. A log file records long-running steps in `logs`, model checkpoints are stored in `data/processed/checkpoints`, and GPU use is resolved safely at runtime.

The default path is CPU. The existing scikit-learn models in this notebook are CPU-only. XGBoost is the only optional GPU-capable model, and it is included only when `xgboost>=2` is installed in the environment. If XGBoost or a CUDA-capable GPU is unavailable, the notebook continues on CPU.
```

- [ ] **Step 4: Insert this code cell immediately after the new markdown cell**

```python
def configure_a_phase_logger(log_dir: Path) -> tuple[logging.Logger, Path]:
    log_path = log_dir / f"{date.today().isoformat()}_A_Phase.log"
    logger = logging.getLogger("energycast.a_phase")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger, log_path


LOGGER, LOG_PATH = configure_a_phase_logger(LOG_DIR)
LOGGER.info("A-phase notebook started.")
LOGGER.info("Project root: %s", ROOT)
LOGGER.info("Log file: %s", LOG_PATH)


USE_GPU = "auto"  # "auto", "cpu", or "gpu"


def nvidia_gpu_available() -> bool:
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def resolve_training_device(use_gpu: str | bool | None) -> str:
    if use_gpu in (False, "cpu", "CPU"):
        return "cpu"
    if nvidia_gpu_available():
        return "cuda"
    if use_gpu in (True, "gpu", "GPU"):
        LOGGER.warning("GPU was requested, but no CUDA-capable GPU was detected. Falling back to CPU.")
    return "cpu"


TRAINING_DEVICE = resolve_training_device(USE_GPU)
XGBOOST_AVAILABLE = importlib.util.find_spec("xgboost") is not None

gpu_support_summary = pd.DataFrame(
    [
        {"model_family": "Dummy, Logistic Regression, KNN, Linear SVM", "gpu_support": "CPU-only scikit-learn estimators"},
        {"model_family": "Decision Tree, Random Forest", "gpu_support": "CPU-only scikit-learn estimators"},
        {
            "model_family": "XGBoost",
            "gpu_support": (
                f"optional; {'available' if XGBOOST_AVAILABLE else 'not installed'}; "
                f"resolved device={TRAINING_DEVICE}"
            ),
        },
    ]
)

LOGGER.info("GPU mode requested=%s, resolved device=%s, xgboost_available=%s", USE_GPU, TRAINING_DEVICE, XGBOOST_AVAILABLE)
display(gpu_support_summary)
```

- [ ] **Step 5: Verify the setup cell behavior**

Run:

```bash
uv run jupyter nbconvert --to notebook --execute notebooks/003_A_Phase.ipynb --output 003_A_Phase.setup_check.ipynb --output-dir /tmp/energycast_a3_setup_check --ExecutePreprocessor.timeout=-1
```

Expected:

```text
notebooks/003_A_Phase.ipynb executes without import errors.
logs/<current-date>_A_Phase.log exists.
The notebook output displays a GPU support table.
```

---

### Task 2: Add Progress Logging to Data Preparation Cells

**Files:**
- Modify: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Append these lines to the end of the data loading code cell**

```python
LOGGER.info(
    "Loaded and joined raw data: %s rows, %s duplicate UTC timestamps, %s missing target rows.",
    f"{len(panel):,}",
    int(panel[JOIN_KEY].duplicated().sum()),
    int(panel[TARGET].isna().sum()),
)
```

- [ ] **Step 2: Append these lines to the end of the feature engineering code cell**

```python
LOGGER.info(
    "Created feature table: %s modeling rows, %s features, high-load threshold %.1f MW.",
    f"{len(model_data):,}",
    len(FEATURE_COLUMNS),
    high_load_threshold_mw,
)
```

- [ ] **Step 3: Append these lines to the end of the chronological split code cell that creates `X_train`, `X_valid`, and `X_reserved_test`**

```python
LOGGER.info(
    "Prepared chronological splits: train=%s rows, validation=%s rows, reserved_test=%s rows.",
    f"{len(X_train):,}",
    f"{len(X_valid):,}",
    f"{len(X_reserved_test):,}",
)
```

- [ ] **Step 4: Verify logging lines are written**

Run the notebook command from Task 1 Step 5.

Expected log entries include:

```text
Loaded and joined raw data
Created feature table
Prepared chronological splits
```

---

### Task 3: Replace Model Training With Checkpoint-Aware Training

**Files:**
- Modify: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Replace the `## Model training` markdown cell with this source**

```markdown
## Model training

The course material emphasizes that no single algorithm is best for every dataset. This notebook therefore compares simple, linear, instance-based, tree-based, ensemble, and margin-based classifiers.

Scaling is applied only where the algorithm needs it: Logistic Regression, KNN, and Linear SVM. Tree models do not require scaling. All imputers and scalers live inside scikit-learn pipelines, so preprocessing is fitted only on the training fold during cross-validation.

This section now uses per-model checkpoints because grid searches and ensemble fitting are the expensive part of the A3 iteration loop. Each checkpoint stores the fitted estimator, its training summary row, and metadata describing the feature set, split contract, model specification, scikit-learn version, and device choice. If the metadata no longer matches, the notebook retrains and overwrites that checkpoint.

GPU acceleration is optional and conservative. The default scikit-learn models remain CPU-only. XGBoost is added only when `xgboost>=2` is installed, and it uses CUDA only when the runtime detects a compatible GPU or `USE_GPU` resolves to `"gpu"` with a detected GPU.
```

- [ ] **Step 2: Replace the model training code cell with this exact source**

```python
def numeric_pipeline(model, *, scale: bool = False) -> Pipeline:
    steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", model))
    return Pipeline(steps)


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set, range)):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def model_slug(model_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", model_name.lower()).strip("_")
    return re.sub(r"_+", "_", slug)


def checkpoint_path_for(model_name: str) -> Path:
    return CHECKPOINT_DIR / f"003_A_Phase__{model_slug(model_name)}.joblib"


def checkpoint_metadata_path_for(model_name: str) -> Path:
    return CHECKPOINT_DIR / f"003_A_Phase__{model_slug(model_name)}.metadata.json"


def checkpoint_metadata_for(model_name: str, spec: dict, cv: TimeSeriesSplit) -> dict:
    return {
        "notebook": "003_A_Phase.ipynb",
        "model_name": model_name,
        "random_state": RANDOM_STATE,
        "target": HIGH_LOAD_LABEL,
        "high_load_quantile": HIGH_LOAD_QUANTILE,
        "high_load_threshold_mw": high_load_threshold_mw,
        "feature_columns": FEATURE_COLUMNS,
        "train_years": list(TRAIN_YEARS),
        "validation_year": VALIDATION_YEAR,
        "reserved_test_year": RESERVED_TEST_YEAR,
        "train_rows": int(len(X_train)),
        "train_index_min": int(X_train.index.min()),
        "train_index_max": int(X_train.index.max()),
        "train_class_counts": {str(key): int(value) for key, value in y_train.value_counts().sort_index().items()},
        "cv": {"type": "TimeSeriesSplit", "n_splits": cv.n_splits},
        "scoring": "f1",
        "param_grid": json_ready(spec["param_grid"]),
        "pipeline_repr": repr(spec["pipeline"]),
        "training_device": TRAINING_DEVICE,
        "xgboost_available": XGBOOST_AVAILABLE,
        "sklearn_version": sklearn.__version__,
    }


def load_checkpoint_if_valid(model_name: str, expected_metadata: dict) -> dict | None:
    checkpoint_path = checkpoint_path_for(model_name)
    if not checkpoint_path.exists():
        return None
    try:
        payload = joblib.load(checkpoint_path)
    except Exception:
        LOGGER.exception("Failed to load checkpoint for %s from %s. Retraining.", model_name, checkpoint_path)
        return None

    saved_metadata = payload.get("metadata")
    if saved_metadata != expected_metadata:
        LOGGER.info("Checkpoint metadata changed for %s. Retraining this model.", model_name)
        return None

    LOGGER.info("Loaded checkpoint for %s from %s.", model_name, checkpoint_path)
    return payload


def save_checkpoint(model_name: str, estimator: Pipeline, training_row: dict, metadata: dict) -> None:
    checkpoint_path = checkpoint_path_for(model_name)
    metadata_path = checkpoint_metadata_path_for(model_name)
    payload = {
        "estimator": estimator,
        "training_row": json_ready(training_row),
        "metadata": metadata,
    }
    temporary_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
    joblib.dump(payload, temporary_path)
    temporary_path.replace(checkpoint_path)
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    LOGGER.info("Saved checkpoint for %s to %s.", model_name, checkpoint_path)


def fit_model_from_spec(model_name: str, spec: dict, cv: TimeSeriesSplit) -> tuple[Pipeline, dict]:
    pipeline = spec["pipeline"]
    param_grid = spec["param_grid"]
    start_time = time.perf_counter()
    LOGGER.info("Training started for %s.", model_name)

    try:
        if param_grid:
            search = GridSearchCV(
                estimator=pipeline,
                param_grid=param_grid,
                scoring="f1",
                cv=cv,
                n_jobs=1,
                error_score="raise",
            )
            search.fit(X_train, y_train)
            estimator = search.best_estimator_
            best_params = search.best_params_
            cv_f1 = float(search.best_score_)
        else:
            cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1", n_jobs=1)
            estimator = pipeline.fit(X_train, y_train)
            best_params = {}
            cv_f1 = float(cv_scores.mean())
    except Exception:
        LOGGER.exception("Training failed for %s.", model_name)
        raise

    elapsed_seconds = time.perf_counter() - start_time
    training_row = {
        "model": model_name,
        "cv_mean_f1": cv_f1,
        "best_params": best_params if best_params else "not tuned",
        "training_seconds": elapsed_seconds,
        "checkpoint_status": "trained",
    }
    LOGGER.info(
        "Training finished for %s in %.1f seconds with cv_mean_f1=%.4f.",
        model_name,
        elapsed_seconds,
        cv_f1,
    )
    return estimator, training_row


def fit_or_load_model(model_name: str, spec: dict, cv: TimeSeriesSplit) -> tuple[Pipeline, dict]:
    expected_metadata = checkpoint_metadata_for(model_name, spec, cv)
    payload = load_checkpoint_if_valid(model_name, expected_metadata)
    if payload is not None:
        training_row = dict(payload["training_row"])
        training_row["checkpoint_status"] = "loaded"
        return payload["estimator"], training_row

    estimator, training_row = fit_model_from_spec(model_name, spec, cv)
    save_checkpoint(model_name, estimator, training_row, expected_metadata)
    return estimator, training_row


def build_optional_xgboost_pipeline() -> Pipeline | None:
    if not XGBOOST_AVAILABLE:
        LOGGER.info("XGBoost is not installed. Skipping optional GPU-capable model.")
        return None

    xgboost = importlib.import_module("xgboost")
    major_version = int(xgboost.__version__.split(".", maxsplit=1)[0])
    if major_version < 2:
        LOGGER.warning("Installed XGBoost version %s is below 2.0. Skipping optional model.", xgboost.__version__)
        return None

    positive_count = int((y_train == 1).sum())
    negative_count = int((y_train == 0).sum())
    scale_pos_weight = negative_count / max(positive_count, 1)

    model = xgboost.XGBClassifier(
        n_estimators=300,
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",
        device=TRAINING_DEVICE,
        subsample=0.9,
        colsample_bytree=0.9,
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    LOGGER.info("Adding optional XGBoost model with device=%s.", TRAINING_DEVICE)
    return numeric_pipeline(model)


model_specs = {
    "Dummy majority baseline": {
        "pipeline": numeric_pipeline(DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)),
        "param_grid": {},
    },
    "Logistic Regression": {
        "pipeline": numeric_pipeline(
            LogisticRegression(class_weight="balanced", max_iter=2_000, random_state=RANDOM_STATE),
            scale=True,
        ),
        "param_grid": {"model__C": [0.1, 1.0, 10.0]},
    },
    "Decision Tree": {
        "pipeline": numeric_pipeline(DecisionTreeClassifier(class_weight="balanced", random_state=RANDOM_STATE)),
        "param_grid": {
            "model__max_depth": [4, 8, 12, None],
            "model__min_samples_leaf": [20, 60],
        },
    },
    "Random Forest": {
        "pipeline": numeric_pipeline(
            RandomForestClassifier(
                n_estimators=200,
                class_weight="balanced_subsample",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )
        ),
        "param_grid": {
            "model__max_depth": [8, 14],
            "model__min_samples_leaf": [10, 30],
        },
    },
    "k-Nearest Neighbors": {
        "pipeline": numeric_pipeline(KNeighborsClassifier(), scale=True),
        "param_grid": {"model__n_neighbors": [5, 15, 31]},
    },
    "Linear SVM": {
        "pipeline": numeric_pipeline(
            LinearSVC(class_weight="balanced", max_iter=10_000, random_state=RANDOM_STATE),
            scale=True,
        ),
        "param_grid": {"model__C": [0.1, 1.0, 10.0]},
    },
}

xgboost_pipeline = build_optional_xgboost_pipeline()
if xgboost_pipeline is not None:
    model_specs["XGBoost optional GPU-capable"] = {
        "pipeline": xgboost_pipeline,
        "param_grid": {
            "model__max_depth": [3, 5],
            "model__learning_rate": [0.05, 0.1],
        },
    }

ts_cv = TimeSeriesSplit(n_splits=3)
trained_models = {}
training_rows = []

LOGGER.info("Starting model training loop for %s model specifications.", len(model_specs))
for index, (model_name, spec) in enumerate(model_specs.items(), start=1):
    LOGGER.info("[%s/%s] Processing %s.", index, len(model_specs), model_name)
    estimator, training_row = fit_or_load_model(model_name, spec, ts_cv)
    trained_models[model_name] = estimator
    training_rows.append(training_row)

training_summary = pd.DataFrame(training_rows).sort_values("cv_mean_f1", ascending=False).reset_index(drop=True)
display(training_summary)
LOGGER.info("Model training loop complete.")
```

- [ ] **Step 3: Verify checkpoints are created**

Run:

```bash
uv run jupyter nbconvert --to notebook --execute notebooks/003_A_Phase.ipynb --output 003_A_Phase.checkpoint_check.ipynb --output-dir /tmp/energycast_a3_checkpoint_check --ExecutePreprocessor.timeout=-1
find data/processed/checkpoints -maxdepth 1 -type f -name '003_A_Phase__*.joblib' -print
find data/processed/checkpoints -maxdepth 1 -type f -name '003_A_Phase__*.metadata.json' -print
```

Expected:

```text
At least six .joblib checkpoint files are printed.
Matching .metadata.json files are printed.
The log contains "Saved checkpoint" on the first run.
```

- [ ] **Step 4: Verify checkpoints are reused**

Run the same `uv run jupyter nbconvert ...` command again.

Expected:

```text
The log contains "Loaded checkpoint" for existing valid model checkpoints.
The second run is faster than the first model-training run.
```

---

### Task 4: Log Evaluation Results and Save A-Phase Artifacts

**Files:**
- Modify: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Append these lines to the end of the validation evaluation code cell**

```python
LOGGER.info(
    "Validation evaluation complete. Selected %s with f1=%.4f and roc_auc=%.4f.",
    best_model_name,
    float(validation_metrics.loc[0, "f1"]),
    float(validation_metrics.loc[0, "roc_auc"]),
)
```

- [ ] **Step 2: Append these lines to the end of the final A-phase conclusion code cell**

```python
training_summary.to_csv(A_PHASE_TRAINING_SUMMARY_PATH, index=False)
validation_metrics.to_csv(A_PHASE_VALIDATION_METRICS_PATH, index=False)

candidate_metadata = {
    "notebook": "003_A_Phase.ipynb",
    "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "selected_model": best_model_name,
    "selection_metric": "f1",
    "tie_breaker": "roc_auc",
    "validation_year": VALIDATION_YEAR,
    "reserved_test_year": RESERVED_TEST_YEAR,
    "reserved_test_used_for_selection": False,
    "high_load_threshold_mw": high_load_threshold_mw,
    "feature_columns": FEATURE_COLUMNS,
    "metrics": json_ready(
        best_row[["accuracy", "precision", "recall", "f1", "roc_auc", "cv_mean_f1"]].to_dict()
    ),
    "checkpoint_dir": str(CHECKPOINT_DIR.relative_to(ROOT)),
    "log_path": str(LOG_PATH.relative_to(ROOT)),
}

joblib.dump(
    {
        "estimator": best_estimator,
        "metadata": candidate_metadata,
    },
    A_PHASE_MODEL_PATH,
)
A_PHASE_MODEL_METADATA_PATH.write_text(
    json.dumps(candidate_metadata, indent=2, sort_keys=True),
    encoding="utf-8",
)

LOGGER.info("Saved training summary to %s.", A_PHASE_TRAINING_SUMMARY_PATH)
LOGGER.info("Saved validation metrics to %s.", A_PHASE_VALIDATION_METRICS_PATH)
LOGGER.info("Saved A-phase candidate model to %s.", A_PHASE_MODEL_PATH)
```

- [ ] **Step 3: Verify artifact files are written**

Run:

```bash
uv run jupyter nbconvert --to notebook --execute notebooks/003_A_Phase.ipynb --output 003_A_Phase.artifact_check.ipynb --output-dir /tmp/energycast_a3_artifact_check --ExecutePreprocessor.timeout=-1
ls -1 data/processed/003_A_Phase_training_summary.csv data/processed/003_A_Phase_validation_metrics.csv models/003_A_Phase_candidate_model.joblib models/003_A_Phase_candidate_model_metadata.json
```

Expected:

```text
All four artifact paths are listed.
models/003_A_Phase_candidate_model_metadata.json contains "reserved_test_used_for_selection": false.
```

---

### Task 5: Preserve A3 Scope in Notebook Text

**Files:**
- Modify: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Append this paragraph to the `## A-phase conclusion` markdown cell**

```markdown
The saved model artifact is an A-phase candidate handoff, not a final C-phase conclusion. The reserved 2019 period remains untouched by model fitting, hyperparameter tuning, model selection, checkpoint validation, and artifact selection.
```

- [ ] **Step 2: Append this paragraph to the `### Limitations and next steps` markdown cell**

```markdown
GPU acceleration is intentionally optional. The default scikit-learn candidates are CPU-only; XGBoost participates only when the environment includes a compatible optional installation. Future C-phase work may compare the saved A-phase candidate against additional final criteria, but should not retroactively change the A-phase validation protocol.
```

- [ ] **Step 3: Verify reserved-test wording**

Run:

```bash
python -c "import json; nb=json.load(open('notebooks/003_A_Phase.ipynb', encoding='utf-8')); text=''.join(''.join(c.get('source', [])) for c in nb['cells']); assert 'reserved 2019 period remains untouched' in text; assert 'XGBoost participates only when' in text"
```

Expected:

```text
The command exits with status 0.
```

---

### Task 6: Full Notebook Validation

**Files:**
- Validate: `notebooks/003_A_Phase.ipynb`

- [ ] **Step 1: Execute the notebook from the repository root**

```bash
uv run jupyter nbconvert --to notebook --execute notebooks/003_A_Phase.ipynb --output 003_A_Phase.executed.ipynb --output-dir /tmp/energycast_a3_full_validation --ExecutePreprocessor.timeout=-1
```

Expected:

```text
Notebook execution completes without an exception.
```

- [ ] **Step 2: Check expected logs and artifacts**

```bash
python -c "from datetime import date; from pathlib import Path; paths=[Path('logs') / f'{date.today().isoformat()}_A_Phase.log', Path('data/processed/003_A_Phase_training_summary.csv'), Path('data/processed/003_A_Phase_validation_metrics.csv'), Path('models/003_A_Phase_candidate_model.joblib'), Path('models/003_A_Phase_candidate_model_metadata.json')]; missing=[str(p) for p in paths if not p.exists()]; assert not missing, missing; print('\n'.join(str(p) for p in paths))"
```

Expected:

```text
The command prints the log, metrics, and model artifact paths.
```

- [ ] **Step 3: Confirm checkpoint reuse is visible**

```bash
python -c "from datetime import date; from pathlib import Path; log_path=Path('logs') / f'{date.today().isoformat()}_A_Phase.log'; text=log_path.read_text(encoding='utf-8'); assert 'Loaded checkpoint' in text or 'Saved checkpoint' in text; print(log_path)"
```

Expected:

```text
The command prints the current A-phase log path.
```

- [ ] **Step 4: Inspect git changes without reverting user work**

```bash
git status --short
git diff -- notebooks/003_A_Phase.ipynb
```

Expected:

```text
`notebooks/003_A_Phase.ipynb` is modified.
Generated artifacts may also appear depending on repository ignore rules.
Existing unrelated user changes, such as `docs/prompts/03_prompts_phase_a.md`, remain untouched.
```

---

## Self-Review Checklist

- Requirement coverage:
  - Checkpointing: Task 3 writes and reuses per-model checkpoints in `data/processed/checkpoints`.
  - Logging: Tasks 1, 2, 3, and 4 configure `logs/<YYYY-MM-DD>_A_Phase.log` and log data loading, training start/end, checkpoint load/save, evaluation, artifact saving, and errors.
  - GPU acceleration: Tasks 1 and 3 add safe optional XGBoost support and document that scikit-learn models remain CPU-only.
  - Clean checkout: XGBoost is optional and import-guarded; CPU-only scikit-learn path remains the default.
  - A3 scope: Tasks 4 and 5 keep 2019 reserved for C phase and label the saved model as an A-phase candidate handoff.
  - Predictable outputs: Task 4 writes metrics and model artifacts to stable paths.
- Placeholder scan: The plan contains no deferred implementation sections.
- Type consistency:
  - `LOGGER`, `LOG_PATH`, `CHECKPOINT_DIR`, `TRAINING_DEVICE`, and `XGBOOST_AVAILABLE` are defined before use.
  - `json_ready` is defined before checkpoint metadata and artifact metadata use it.
  - `best_row`, `best_model_name`, and `best_estimator` already exist before the conclusion cell saves artifacts.
