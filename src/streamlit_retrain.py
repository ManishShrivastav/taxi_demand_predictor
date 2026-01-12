import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
from src.model import load_model, train_model
from src.data import load_validation_data
from sklearn.metrics import mean_absolute_error
import joblib

MODEL_PATH = os.getenv('MODEL_PATH', 'models/latest_model.pkl')
DEFAULT_THRESHOLD = 10.0

st.title('Taxi Demand Model Monitoring & Retraining')

# Load validation data
X_val, y_val = load_validation_data()

# Load model
model = load_model(MODEL_PATH)
preds = model.predict(X_val)
mae = mean_absolute_error(y_val, preds)

st.metric('Current MAE', f'{mae:.2f}')

threshold = st.number_input('MAE Threshold', value=DEFAULT_THRESHOLD)

if mae > threshold:
    st.warning(f'MAE {mae:.2f} exceeds threshold {threshold}. Retraining recommended!')
    if st.button('Retrain Model'):
        with st.spinner('Retraining...'):
            model = train_model()
            joblib.dump(model, MODEL_PATH)
            st.success('Model retrained and saved!')
else:
    st.success(f'MAE {mae:.2f} is within threshold {threshold}. No retraining needed.')

if st.button('Refresh MAE'):
    st.experimental_rerun()
