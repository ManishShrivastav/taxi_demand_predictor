# 🚕 NYC Taxi Demand Predictor — Real-Time MLOps System

[![Feature Pipeline](https://github.com/ManishShrivastav/taxi_demand_predictor/actions/workflows/feature_pipeline.yaml/badge.svg)](https://github.com/ManishShrivastav/taxi_demand_predictor/actions/workflows/feature_pipeline.yaml)
[![Inference Pipeline](https://github.com/ManishShrivastav/taxi_demand_predictor/actions/workflows/inference_pipeline.yaml/badge.svg)](https://github.com/ManishShrivastav/taxi_demand_predictor/actions/workflows/inference_pipeline.yaml)

> **An end-to-end MLOps system for predicting hourly taxi demand across 260+ NYC zones, featuring automated pipelines, a feature store, and real-time monitoring dashboards.**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Hopsworks](https://img.shields.io/badge/Feature%20Store-Hopsworks-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?logo=github-actions)
![LightGBM](https://img.shields.io/badge/Model-LightGBM-green)

---

## 🎯 Project Focus

**This is NOT a typical ML project focused on model accuracy.**

This project demonstrates **production ML engineering** — taking a trained model and building the infrastructure to:
- Serve predictions in real-time
- Automate data and inference pipelines
- Monitor model performance in production
- Handle the full MLOps lifecycle

| What This Project IS | What This Project IS NOT |
|---------------------|--------------------------|
| ✅ Feature Store architecture | ❌ Hyperparameter tuning focus |
| ✅ Automated hourly pipelines | ❌ Model comparison studies |
| ✅ Real-time inference system | ❌ Deep learning experiments |
| ✅ Production monitoring | ❌ Kaggle-style competitions |
| ✅ CI/CD with GitHub Actions | ❌ Accuracy optimization |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NYC TAXI DEMAND PREDICTOR                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   RAW DATA      │    │  FEATURE STORE  │    │    MODEL        │         │
│  │   (NYC TLC)     │───▶│   (Hopsworks)   │◀───│   REGISTRY      │         │
│  └─────────────────┘    └────────┬────────┘    └─────────────────┘         │
│                                  │                                          │
│         ┌────────────────────────┼────────────────────────┐                │
│         │                        │                        │                │
│         ▼                        ▼                        ▼                │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐          │
│  │  FEATURE    │         │  TRAINING   │         │  INFERENCE  │          │
│  │  PIPELINE   │         │  PIPELINE   │         │  PIPELINE   │          │
│  │  (Hourly)   │         │  (On-demand)│         │  (Hourly)   │          │
│  └─────────────┘         └─────────────┘         └──────┬──────┘          │
│         │                                                │                 │
│         │              GitHub Actions                    │                 │
│         └────────────────────────────────────────────────┘                 │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────┐                             │
│                    │    STREAMLIT APPS       │                             │
│                    │  ┌───────────────────┐  │                             │
│                    │  │ Prediction UI     │  │                             │
│                    │  │ Monitoring UI     │  │                             │
│                    │  └───────────────────┘  │                             │
│                    └─────────────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Language** | Python 3.11 | Core development |
| **Feature Store** | Hopsworks | Feature storage, versioning, and serving |
| **ML Framework** | LightGBM | Gradient boosting for demand prediction |
| **Orchestration** | GitHub Actions | Hourly automated pipeline execution |
| **Frontend** | Streamlit | Interactive dashboards |
| **Visualization** | Plotly, Folium | Interactive charts and maps |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Geospatial** | GeoPandas, Shapely | NYC zone mapping |
| **Experiment Tracking** | Optuna | Hyperparameter optimization (training) |

---

## 📊 Data Pipeline

### Data Flow

```
NYC TLC Raw Data → Feature Engineering → Time-Series Features → Model Training → Predictions
      │                    │                      │                    │            │
      ▼                    ▼                      ▼                    ▼            ▼
   Parquet            Hourly                 672 lag              Hopsworks     Feature
    Files           Aggregation             features              Registry      Store
```

### Feature Engineering

The model uses **672 lag features** (28 days × 24 hours) for each of the 260+ NYC taxi zones:

```python
features = [
    'rides_previous_1_hour',
    'rides_previous_2_hour',
    ...
    'rides_previous_672_hour'  # 28 days back
]
```

---

## 🔄 Pipeline Architecture

### 1. Feature Pipeline (`hourly-taxi-demand-feature-pipeline`)
- **Trigger**: Runs every hour via cron schedule
- **Purpose**: Fetches latest taxi ride data, transforms into time-series features
- **Output**: Updates `time_series_hourly_feature_group` in Hopsworks

### 2. Inference Pipeline (`hourly-taxi-demand-inference-pipeline`)
- **Trigger**: Automatically runs after feature pipeline completes
- **Purpose**: Generates predictions for the next hour across all zones
- **Output**: Saves predictions to `model_predictions_feature_group`

### Pipeline Chaining
```yaml
# inference_pipeline.yaml
on:
  workflow_run:
    workflows: ["hourly-taxi-demand-feature-pipeline"]
    types:
      - completed
```

---

## 📱 Streamlit Applications

### 1. Prediction Dashboard (`frontend.py`)
Real-time visualization of predicted taxi demand:
- Interactive NYC map with zone-level predictions
- Time-series charts for selected zones
- Hourly demand forecasts

### 2. Monitoring Dashboard (`frontend_monitoring.py`)
Production model monitoring:
- MAE (Mean Absolute Error) tracking hour-by-hour
- Per-location performance analysis
- Predictions vs. actuals comparison

---

## 🗂️ Project Structure

```
taxi_demand_predictor/
│
├── 📁 .github/workflows/          # CI/CD Pipelines
│   ├── feature_pipeline.yaml      # Hourly feature updates
│   └── inference_pipeline.yaml    # Hourly predictions
│
├── 📁 data/
│   ├── raw/                       # Raw taxi ride data
│   ├── transformed/               # Processed time-series data
│   └── taxi_zones/                # NYC zone shapefiles
│
├── 📁 notebooks/                  # Development & Pipeline Notebooks
│   ├── 01-05: Data processing & visualization
│   ├── 06-10: Model development & tuning
│   ├── 11: Feature store backfill
│   ├── 12: Feature pipeline (production)
│   ├── 13: Training pipeline
│   └── 14: Inference pipeline (production)
│
├── 📁 src/                        # Source Code Modules
│   ├── config.py                  # Configuration & secrets
│   ├── data.py                    # Data loading utilities
│   ├── feature_store_api.py       # Hopsworks API wrapper
│   ├── inference.py               # Inference logic
│   ├── model.py                   # Model training utilities
│   ├── monitoring.py              # MAE calculation & monitoring
│   ├── frontend.py                # Prediction Streamlit app
│   └── frontend_monitoring.py     # Monitoring Streamlit app
│
├── 📁 models/                     # Local model artifacts
├── 📁 images/                     # Documentation images
│
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Hopsworks account (free tier available)
- GitHub account (for Actions)

### Installation

```bash
# Clone the repository
git clone https://github.com/ManishShrivastav/taxi_demand_predictor.git
cd taxi_demand_predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:
```env
HOPSWORKS_API_KEY=your_api_key_here
```

2. For Streamlit Cloud deployment, add the secret in your app settings.

3. For GitHub Actions, add `HOPSWORKS_API_KEY` as a repository secret.

### Running Locally

```bash
# Run prediction dashboard
streamlit run src/frontend.py

# Run monitoring dashboard
streamlit run src/frontend_monitoring.py
```

---

## 📈 Model Performance

The LightGBM model is trained on 28 days of historical data and evaluated using:

| Metric | Description |
|--------|-------------|
| **MAE** | Mean Absolute Error — average prediction error in rides |
| **Hourly Tracking** | Performance monitored continuously via dashboards |

---

## 🔑 Key MLOps Concepts Demonstrated

### 1. **Feature Store Pattern**
- Centralized feature repository (Hopsworks)
- Feature versioning and lineage
- Point-in-time correct feature serving

### 2. **Pipeline Orchestration**
- Event-driven pipeline chaining
- Automated hourly execution
- Failure handling and artifact logging

### 3. **Model Registry**
- Versioned model storage
- Model metadata tracking
- Seamless model loading for inference

### 4. **Production Monitoring**
- Real-time MAE tracking
- Predictions vs. actuals comparison
- Location-level performance analysis

### 5. **Infrastructure as Code**
- GitHub Actions YAML workflows
- Reproducible pipeline definitions
- Secret management

---

## 🛣️ Future Enhancements

- [ ] Add alerting when MAE exceeds threshold
- [ ] Implement model retraining pipeline
- [ ] Add A/B testing infrastructure
- [ ] Integrate weather data as features
- [ ] Add data drift detection
- [ ] Implement feature importance monitoring

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Manish Shrivastav**

- Building production ML systems
- Focus on MLOps and ML Engineering
- [GitHub](https://github.com/ManishShrivastav)

---

## 🙏 Acknowledgments

- **Data Source**: [NYC Taxi and Limousine Commission (TLC)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Feature Store**: [Hopsworks](https://www.hopsworks.ai/)
- **Inspiration**: Real-world MLOps practices from industry

---

<p align="center">
  <i>Built with ❤️ to demonstrate real-world MLOps practices</i>
</p>
