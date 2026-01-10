# 📦 Source Code Modules

This directory contains the core Python modules that power the taxi demand prediction system.

---

## 🗂️ Module Overview

| Module | Purpose |
|--------|---------|
| `config.py` | Central configuration and environment variables |
| `paths.py` | File path constants and utilities |
| `data.py` | Data loading and preprocessing utilities |
| `data_split.py` | Train/validation/test splitting logic |
| `feature_store_api.py` | Hopsworks Feature Store wrapper |
| `model.py` | Model training and evaluation utilities |
| `inference.py` / `inference_1.py` | Batch inference logic |
| `monitoring.py` | Model performance monitoring |
| `plot.py` | Visualization utilities |
| `frontend.py` | Streamlit prediction dashboard |
| `frontend_monitoring.py` | Streamlit monitoring dashboard |
| `simple_frontend.py` | Lightweight prediction UI |

---

## 🔧 Configuration (`config.py`)

Central configuration file managing:

```python
# Hopsworks Settings
HOPSWORKS_PROJECT_NAME = 'nyc_taxiride_demand'
HOPSWORKS_API_KEY = <from secrets>

# Feature Store
FEATURE_GROUP_NAME = 'time_series_hourly_feature_group'
FEATURE_GROUP_VERSION = 1
FEATURE_VIEW_NAME = 'time_series_hourly_feature_view'
FEATURE_VIEW_VERSION = 1

# Model
MODEL_NAME = 'taxi_demand_predictor_next_hour'
MODEL_VERSION = 1
N_FEATURES = 672  # 28 days × 24 hours

# Predictions
FEATURE_GROUP_MODEL_PREDICTIONS = 'model_predictions_feature_group'
FEATURE_VIEW_MONITORING = 'monitoring_feature_view'
```

**Secret Management**: Supports both Streamlit secrets and environment variables.

---

## 🗄️ Feature Store API (`feature_store_api.py`)

Wrapper for Hopsworks Feature Store operations:

```python
from src.feature_store_api import get_feature_store, get_feature_group

# Get feature store connection
fs = get_feature_store()

# Get or create feature group
fg = get_feature_group(name='my_feature_group')
```

**Key Functions**:
- `get_hopsworks_project()` — Authenticate and get project
- `get_feature_store()` — Get feature store instance
- `get_feature_group()` — Get or create feature groups

---

## 🔮 Inference (`inference.py`)

Batch inference logic for generating predictions:

```python
from src.inference import (
    load_batch_of_features_from_store,
    load_model_from_registry,
    get_model_predictions
)

# Load features for current hour
features = load_batch_of_features_from_store(current_date)

# Load model from Hopsworks registry
model = load_model_from_registry()

# Generate predictions
predictions = get_model_predictions(model, features)
```

**Features**:
- Loads 672 lag features per location
- Handles missing data gracefully
- Returns predictions with location IDs

---

## 📊 Monitoring (`monitoring.py`)

Compare predictions with actual values:

```python
from src.monitoring import load_predictions_and_actual_values_from_store

# Get predictions vs actuals for date range
monitoring_df = load_predictions_and_actual_values_from_store(
    from_date=start,
    to_date=end
)
```

**Returns DataFrame with**:
- `pickup_location_id`
- `pickup_hour`
- `predicted_demand`
- `rides` (actual)

---

## 🖥️ Streamlit Apps

### Prediction Dashboard (`frontend.py`)

Main user-facing dashboard showing:
- 🗺️ Interactive NYC map with demand predictions
- 📈 Time-series visualizations
- 🔄 Real-time data refresh

### Monitoring Dashboard (`frontend_monitoring.py`)

MLOps monitoring interface showing:
- 📉 MAE trends hour-by-hour
- 🎯 Per-location performance
- ⚠️ Data availability status

---

## 🛠️ Utilities

### `data.py`
- `load_raw_data()` — Load NYC TLC parquet files
- `validate_raw_data()` — Data quality checks
- `transform_raw_data_into_ts_data()` — Convert to hourly time-series

### `data_split.py`
- `train_test_split()` — Temporal train/test splitting
- Ensures no data leakage in time-series

### `plot.py`
- `plot_ts()` — Time-series visualization
- `plot_prediction_vs_actual()` — Model evaluation charts

### `paths.py`
- `RAW_DATA_DIR` — Raw data directory
- `TRANSFORMED_DATA_DIR` — Processed data directory
- `MODELS_DIR` — Model artifacts directory

---

## 🧪 Usage Examples

### Load Data and Generate Predictions

```python
from datetime import datetime, timezone
import pandas as pd
from src.inference import (
    load_batch_of_features_from_store,
    load_model_from_registry,
    get_model_predictions
)

# Current hour (UTC)
current_date = pd.to_datetime(datetime.now(timezone.utc)).floor('h')

# Load features
features = load_batch_of_features_from_store(current_date)

# Load model
model = load_model_from_registry()

# Predict
predictions = get_model_predictions(model, features)
predictions['pickup_hour'] = current_date
```

### Monitor Model Performance

```python
from datetime import timedelta
from src.monitoring import load_predictions_and_actual_values_from_store
from sklearn.metrics import mean_absolute_error

# Get last 7 days of predictions vs actuals
monitoring_df = load_predictions_and_actual_values_from_store(
    from_date=current_date - timedelta(days=7),
    to_date=current_date
)

# Calculate overall MAE
mae = mean_absolute_error(
    monitoring_df['rides'],
    monitoring_df['predicted_demand']
)
print(f"7-day MAE: {mae:.2f} rides")
```

---

## 📝 Notes

- All modules use UTC timestamps for consistency
- Feature store operations require `HOPSWORKS_API_KEY`
- Streamlit apps automatically handle secret management
