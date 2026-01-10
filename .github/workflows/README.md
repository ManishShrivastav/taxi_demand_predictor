# ⚙️ GitHub Actions Workflows

Automated CI/CD pipelines for production ML operations.

---

## 🔄 Pipeline Overview

```
┌─────────────────────────┐         ┌─────────────────────────┐
│   Feature Pipeline      │────────▶│   Inference Pipeline    │
│   (Hourly @ :00)        │ triggers│   (After feature done)  │
└─────────────────────────┘         └─────────────────────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│ Update Feature Store    │         │ Generate Predictions    │
│ with latest ride data   │         │ Save to Feature Store   │
└─────────────────────────┘         └─────────────────────────┘
```

---

## 📋 Workflows

### 1. Feature Pipeline (`feature_pipeline.yaml`)

**Purpose**: Fetch latest taxi data and update the feature store.

| Property | Value |
|----------|-------|
| **Schedule** | Every hour (`0 * * * *`) |
| **Trigger** | Cron schedule + Manual dispatch |
| **Runtime** | ~5 minutes |
| **Notebook** | `12_feature_pipeline.ipynb` |

**Workflow Steps**:
1. ✅ Checkout repository
2. ✅ Set up Python 3.11
3. ✅ Cache pip dependencies
4. ✅ Install requirements
5. ✅ Execute feature pipeline notebook
6. ✅ Upload execution logs as artifact

### 2. Inference Pipeline (`inference_pipeline.yaml`)

**Purpose**: Generate predictions using the latest features and trained model.

| Property | Value |
|----------|-------|
| **Trigger** | After feature pipeline completes |
| **Runtime** | ~4 minutes |
| **Notebook** | `14_inference_pipeline.ipynb` |

**Workflow Steps**:
1. ✅ Checkout repository
2. ✅ Set up Python 3.11
3. ✅ Cache pip dependencies
4. ✅ Install requirements
5. ✅ Execute inference pipeline notebook
6. ✅ Upload execution logs as artifact

---

## 🔗 Pipeline Chaining

The inference pipeline is **event-driven**, triggered by the feature pipeline:

```yaml
# inference_pipeline.yaml
on:
  workflow_run:
    workflows: ["hourly-taxi-demand-feature-pipeline"]
    types:
      - completed
```

This ensures:
- ✅ Fresh features are available before inference
- ✅ No race conditions between pipelines
- ✅ Clear dependency chain

---

## 🔐 Secrets Required

Configure these in **Repository Settings → Secrets and Variables → Actions**:

| Secret | Description |
|--------|-------------|
| `HOPSWORKS_API_KEY` | API key for Hopsworks feature store |

---

## 📊 Monitoring Runs

### View Workflow Status

1. Go to repository → **Actions** tab
2. Select workflow (`hourly-taxi-demand-feature-pipeline` or `hourly-taxi-demand-inference-pipeline`)
3. View run history and status

### Download Execution Logs

Each run saves the executed notebook as an artifact:
1. Click on a workflow run
2. Scroll to **Artifacts** section
3. Download `notebook-logs`

---

## 🛠️ Manual Trigger

Both workflows support manual dispatch for testing:

1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Choose branch and run

---

## ⏰ Cron Schedule Explained

```yaml
cron: '0 * * * *'
```

| Field | Value | Meaning |
|-------|-------|---------|
| Minute | `0` | At minute 0 |
| Hour | `*` | Every hour |
| Day | `*` | Every day |
| Month | `*` | Every month |
| Weekday | `*` | Every weekday |

**Result**: Runs at the start of every hour (00:00, 01:00, 02:00, ...)

---

## 🔧 Workflow Configuration

### Environment Variables

```yaml
env:
  HOPSWORKS_API_KEY: ${{ secrets.HOPSWORKS_API_KEY }}
  PYTHONPATH: ${{ github.workspace }}
```

### Caching Strategy

Pip dependencies are cached to speed up runs:

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

---

## 📝 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `HOPSWORKS_API_KEY not set` | Add secret in repository settings |
| `Module not found` | Check `PYTHONPATH` is set correctly |
| `Feature view not found` | Run backfill notebook first |
| `Timeout` | Check Hopsworks API status |

### Viewing Logs

1. Click on failed run
2. Expand failed step
3. View stdout/stderr
4. Download notebook artifact for full output

---

## 🔗 Related Files

- Feature notebook: `notebooks/12_feature_pipeline.ipynb`
- Inference notebook: `notebooks/14_inference_pipeline.ipynb`
- Requirements: `requirements.txt`
- Configuration: `src/config.py`
