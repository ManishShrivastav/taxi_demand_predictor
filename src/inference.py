from datetime import datetime, timedelta

import hopsworks
from hsfs.feature_store import FeatureStore
import pandas as pd
import numpy as np

import src.config as config

def get_hopsworks_project() -> hopsworks.project.Project:

    return hopsworks.login(
        project=config.HOPSWORKS_PROJECT_NAME,
        api_key_value=config.HOPSWORKS_API_KEY
    )

def get_feature_store() -> FeatureStore:
    project = get_hopsworks_project()
    return project.get_feature_store()

def get_model_predictions(model, features: pd.DataFrame) -> pd.DataFrame:
    """"""

    # past rides_columns = [c for c in features.columns if c.startswith('rides_)]
    predictions = model.predict(features)

    results = pd.DataFrame()
    results['pickup_location_id'] = features['pickup_location_id'].values
    results['predicted_demand'] = predictions.round(0)

    return results


def load_batch_of_features_from_store(current_date: datetime,) -> pd.DataFrame:

    feature_store = get_feature_store()

    n_features = config.N_FEATURES

    print(f'Fetching all available data from feature store')
    feature_view = feature_store.get_feature_view(
        name=config.FEATURE_VIEW_NAME,
        version=config.FEATURE_VIEW_VERSION
    )

    # Use training data to avoid Query Service issues
    ts_data, _ = feature_view.training_data(
        description='Batch inference data'
    )
    ts_data['pickup_hour'] = pd.to_datetime(ts_data['pickup_hour'])
    
    # Remove duplicates (keep latest entry for each location/hour)
    ts_data = ts_data.drop_duplicates(subset=['pickup_location_id', 'pickup_hour'], keep='last')
    
    # Find the most recent data available and use that as reference
    max_hour = ts_data['pickup_hour'].max()
    fetch_data_to = max_hour
    fetch_data_from = fetch_data_to - timedelta(hours=n_features - 1)
    
    print(f'Using data from {fetch_data_from} to {fetch_data_to}')
    ts_data = ts_data[ts_data.pickup_hour.between(fetch_data_from, fetch_data_to)]

    # validate we are not missing data in the feature store
    location_ids = ts_data['pickup_location_id'].unique()
    expected_rows = n_features * len(location_ids)
    actual_rows = len(ts_data)
    
    if actual_rows != expected_rows:
        print(f"Warning: Time-series data is incomplete. Expected {expected_rows} rows, got {actual_rows} rows.")
        print(f"Expected {n_features} hours per location, but data may be missing for some hours.")
        # Filter to only locations with complete data
        location_counts = ts_data.groupby('pickup_location_id').size()
        complete_locations = location_counts[location_counts == n_features].index
        ts_data = ts_data[ts_data['pickup_location_id'].isin(complete_locations)]
        location_ids = ts_data['pickup_location_id'].unique()
        print(f"Proceeding with {len(location_ids)} locations that have complete data.")

    if len(location_ids) == 0:
        raise ValueError(f"No locations have complete data ({n_features} hours). "
                        f"Please run the feature pipeline to populate the feature store with recent data.")

    # sort data by location and time
    ts_data.sort_values(by=['pickup_location_id', 'pickup_hour'], inplace=True)
    print(f'Processing {len(location_ids)} locations')

    # transpose time-series data as a feature vector, for each location_id
    x = np.ndarray(shape=(len(location_ids), n_features), dtype=np.float32)
    for i, location_id in enumerate(location_ids):
        ts_data_i = ts_data.loc[ts_data.pickup_location_id == location_id, :]
        ts_data_i = ts_data_i.sort_values(by=['pickup_hour'])
        x[i, :] = ts_data_i['rides'].values

    features = pd.DataFrame(
        x,
        columns=[f'rides_previous_{i+1}_hour' for i in reversed(range(n_features))]
    )

    features['pickup_hour'] = fetch_data_to + timedelta(hours=1)
    features['pickup_location_id'] = location_ids

    return features

def load_model_from_registry():

    import joblib
    from pathlib import Path

    project = get_hopsworks_project()
    model_registry = project.get_model_registry()

    model = model_registry.get_model(
        name=config.MODEL_NAME,
        version=config.MODEL_VERSION
    )

    model_dir = model.download()
    model = joblib.load(Path(model_dir) / 'model.pkl')

    return model

