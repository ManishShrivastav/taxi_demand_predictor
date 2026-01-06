import os
from dotenv import load_dotenv

from src.paths import PARENT_DIR

# load key-value pairs from .env file located in the parent directory
load_dotenv(PARENT_DIR / '.env')

HOPSWORKS_PROJECT_NAME = 'nyc_taxiride_demand'

# Try Streamlit secrets first, then environment variable
try:
    import streamlit as st
    HOPSWORKS_API_KEY = st.secrets["HOPSWORKS_API_KEY"]
except:
    try:
        HOPSWORKS_API_KEY = os.environ['HOPSWORKS_API_KEY']
    except:
        raise Exception('Set HOPSWORKS_API_KEY in Streamlit secrets or .env file')

FEATURE_GROUP_NAME = 'time_series_hourly_feature_group'
FEATURE_GROUP_VERSION = 1
FEATURE_VIEW_NAME = 'time_series_hourly_feature_view'
FEATURE_VIEW_VERSION = 1
MODEL_NAME = 'taxi_demand_predictor_next_hour'
MODEL_VERSION = 1

# Number of historical hours used as features (28 days * 24 hours)
N_FEATURES = 24 * 28