import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from src.model import train_model, load_model
from src.data import load_validation_data

MAE_THRESHOLD = float(os.getenv('MAE_THRESHOLD', 10.0))  # Default threshold
MODEL_PATH = os.getenv('MODEL_PATH', 'models/latest_model.pkl')


def get_current_mae(model, X_val, y_val):
    preds = model.predict(X_val)
    return mean_absolute_error(y_val, preds)


def main():
    # Load validation data
    X_val, y_val = load_validation_data()

    # Load latest model
    model = load_model(MODEL_PATH)
    mae = get_current_mae(model, X_val, y_val)
    print(f"Current MAE: {mae}")

    if mae > MAE_THRESHOLD:
        print(f"MAE {mae} exceeds threshold {MAE_THRESHOLD}. Retraining...")
        model = train_model()
        joblib.dump(model, MODEL_PATH)
        print("Model retrained and saved.")
    else:
        print(f"MAE {mae} is within threshold {MAE_THRESHOLD}. No retraining needed.")

if __name__ == "__main__":
    main()
