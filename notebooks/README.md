# 📓 Notebooks

This directory contains Jupyter notebooks organized in a logical workflow — from data exploration to production pipelines.

---

## 🗂️ Notebook Overview

| # | Notebook | Purpose | Type |
|---|----------|---------|------|
| 01 | `01_load_and_validate_raw_data.ipynb` | Load & validate NYC taxi data | Exploration |
| 02 | `02_transform_raw_data_into_ts_data.ipynb` | Convert to hourly time-series | Processing |
| 03 | `03_transform_ts_data_into_features_and_targets.ipynb` | Create lag features | Feature Eng. |
| 04 | `04_transform_raw_data_into_features_and_targets.ipynb` | End-to-end feature pipeline | Feature Eng. |
| 05 | `05_visualize_training_data.ipynb` | Explore training data | Visualization |
| 06 | `06_baseline_model.ipynb` | Simple baseline model | Modeling |
| 07 | `07_xgboost_model.ipynb` | XGBoost experiments | Modeling |
| 08 | `08_lightgbm_model.ipynb` | LightGBM experiments | Modeling |
| 09 | `09_lightgbm_model_with_feature_engineering.ipynb` | LightGBM + features | Modeling |
| 10 | `10_lightgbm_model_with_hyperparameter_tuning.ipynb` | Optuna tuning | Modeling |
| 11 | `11_backfill_feature_store.ipynb` | Populate Hopsworks | Infrastructure |
| 12 | `12_feature_pipeline.ipynb` | **Production feature pipeline** | 🚀 Production |
| 13 | `13_model_training_pipeline.ipynb` | Train & register model | Training |
| 14 | `14_inference_pipeline.ipynb` | **Production inference pipeline** | 🚀 Production |

---

## 📚 Notebook Categories

### 🔍 Data Exploration (01-05)

**Purpose**: Understand the data, validate quality, and visualize patterns.

```
01 → Load raw parquet files from NYC TLC
02 → Transform to hourly aggregates per zone
03 → Create 672 lag features (28 days × 24 hours)
04 → Full transformation pipeline
05 → Visualize time-series patterns
```

### 🤖 Model Development (06-10)

**Purpose**: Develop and compare models (educational, not production focus).

```
06 → Baseline: simple average-based predictions
07 → XGBoost: gradient boosting experiments
08 → LightGBM: fast gradient boosting
09 → LightGBM + additional features
10 → Hyperparameter tuning with Optuna
```

**Note**: This project focuses on MLOps, not model optimization. These notebooks exist to show a realistic workflow, but the "final" model is treated as given.

### 🏗️ Infrastructure (11)

**Purpose**: Set up the feature store with historical data.

```
11 → Backfill Hopsworks feature store with historical time-series data
```

### 🚀 Production Pipelines (12-14)

**Purpose**: Automated pipelines running in production via GitHub Actions.

```
12 → Feature Pipeline: Fetch new data → Transform → Push to feature store
13 → Training Pipeline: Pull features → Train model → Register in model registry
14 → Inference Pipeline: Load features → Generate predictions → Save to feature store
```

---

## 🔄 Production Pipeline Details

### Feature Pipeline (`12_feature_pipeline.ipynb`)

**Runs**: Every hour via GitHub Actions

```python
# Workflow
1. Fetch latest taxi ride data
2. Transform to hourly time-series format
3. Push to Hopsworks feature group
```

**GitHub Actions Trigger**:
```yaml
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
```

### Inference Pipeline (`14_inference_pipeline.ipynb`)

**Runs**: After feature pipeline completes

```python
# Workflow
1. Load 672 lag features from feature store
2. Load model from Hopsworks registry
3. Generate predictions for next hour
4. Save predictions to feature store
```

**GitHub Actions Trigger**:
```yaml
on:
  workflow_run:
    workflows: ["hourly-taxi-demand-feature-pipeline"]
    types:
      - completed
```

---

## 🧪 Running Notebooks Locally

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variable
export HOPSWORKS_API_KEY=your_api_key_here
```

### Execution Order

For a fresh setup, run notebooks in order:

```bash
# 1. Data exploration
jupyter notebook 01_load_and_validate_raw_data.ipynb

# 2. Feature engineering
jupyter notebook 02_transform_raw_data_into_ts_data.ipynb
jupyter notebook 03_transform_ts_data_into_features_and_targets.ipynb

# 3. Backfill feature store (one-time)
jupyter notebook 11_backfill_feature_store.ipynb

# 4. Train and register model (one-time)
jupyter notebook 13_model_training_pipeline.ipynb

# 5. Test inference locally
jupyter notebook 14_inference_pipeline.ipynb
```

---

## 📊 Key Concepts by Notebook

### Feature Engineering (03)

Creates **672 lag features** per location:

```python
# For each pickup_location_id:
rides_previous_1_hour   # 1 hour ago
rides_previous_2_hour   # 2 hours ago
...
rides_previous_672_hour # 28 days ago (672 hours)
```

### Model Training (13)

Trains LightGBM and registers in Hopsworks:

```python
# Train
model = LGBMRegressor()
model.fit(X_train, y_train)

# Register
model_registry.register_model(
    name='taxi_demand_predictor_next_hour',
    model=model
)
```

### Inference (14)

Generates hourly predictions:

```python
# Load features for current hour
features = load_batch_of_features_from_store(current_date)

# Predict
predictions = model.predict(features)

# Save to feature store
feature_group.insert(predictions)
```

---

## ⚠️ Important Notes

1. **UTC Timestamps**: All pipelines use UTC for consistency
2. **Feature Store**: Requires Hopsworks API key
3. **Idempotency**: Pipelines handle re-runs gracefully
4. **Logging**: GitHub Actions saves notebook outputs as artifacts

---

## 🔗 Related Files

- **GitHub Actions**: `.github/workflows/`
- **Source Modules**: `src/`
- **Configuration**: `src/config.py`
