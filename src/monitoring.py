# """
# Monitoring module for comparing predictions with actual values
# """
# from datetime import datetime, timedelta

# import pandas as pd

# from src.feature_store_api import get_feature_store, get_feature_group
# import src.config as config

# def load_predictions_and_actual_values_from_store(
#     from_date: datetime,
#     to_date: datetime
# ) -> pd.DataFrame:
#     """
#     Fetches model predictions and actual ride values from the feature store
#     for a given time range, then merges them for comparison.
    
#     Args:
#         from_date (datetime): Start datetime (rounded hour)
#         to_date (datetime): End datetime (rounded hour)
    
#     Returns:
#         pd.DataFrame: DataFrame with columns:
#             - pickup_location_id
#             - pickup_hour
#             - predicted_demand
#             - rides (actual demand)
#     """
#     # feature groups we need to merge
#     predictions_fg = get_feature_group(name=config.FEATURE_GROUP_MODEL_PREDICTIONS)
#     actuals_fg = get_feature_group(name=config.FEATURE_GROUP_NAME)

#     # query to join the 2 feature groups by 'pickup_hour' and 'pickup_location_id'
#     query = predictions_fg.select_all() \
#         .join(actuals_fg.select_all(), on=['pickup_hour', 'pickup_location_id']) \
#         .filter(predictions_fg.pickup_hour >= from_date) \
#         .filter(predictions_fg.pickup_hour <= to_date)
    
#     # create the feature view 'config.FEATURE_VIEW_MONITORING' if it doesn't exist yet
#     feature_store = get_feature_store()
#     try:
#         # create feature view as it doesn't exist yet
#         feature_store.create_feature_view(
#             name=config.FEATURE_VIEW_MONITORING,
#             version=1,
#             query=query
#         )
#     except:
#         print('Feature view already existed. Skip creation')

#     # feature view
#     monitoring_fv = feature_store.get_feature_view(
#         name=config.FEATURE_VIEW_MONITORING,
#         version=1
#     )

#     # fetch data from the feature view 
#     # fetch predicted and actual values from the last 30 days
#     monitoring_df = monitoring_fv.get_batch_data(
#         start_time = from_date - timedelta(days=7),
#         end_time = to_date + timedelta(days=7)
#     )

#     monitoring_df = monitoring_df[monitoring_df.pickup_hour.between(from_date, to_date)]

#     return monitoring_df


"""
Monitoring module for comparing predictions with actual values
"""
from datetime import datetime, timedelta

import pandas as pd
from hsfs.client.exceptions import RestAPIError

from src.feature_store_api import get_feature_store, get_feature_group
import src.config as config


def load_predictions_and_actual_values_from_store(
    from_date: datetime,
    to_date: datetime
) -> pd.DataFrame:
    """
    Fetches model predictions and actual ride values from the feature store
    for a given time range, then merges them for comparison.
    
    Args:
        from_date (datetime): Start datetime (rounded hour)
        to_date (datetime): End datetime (rounded hour)
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            - pickup_location_id
            - pickup_hour
            - predicted_demand
            - rides (actual demand)
    """
    feature_store = get_feature_store()
    
    # Read predictions directly from feature group
    print("Fetching predictions from feature group...")
    predictions_fg = feature_store.get_feature_group(
        name=config.FEATURE_GROUP_MODEL_PREDICTIONS,
        version=1
    )
    predictions_df = predictions_fg.read()
    print(f"Predictions shape: {predictions_df.shape}")
    
    if predictions_df.empty:
        print("WARNING: No predictions found in feature store!")
        return pd.DataFrame(columns=['pickup_location_id', 'predicted_demand', 'pickup_hour', 'rides'])
    
    predictions_df['pickup_hour'] = pd.to_datetime(predictions_df['pickup_hour'])
    print(f"Predictions date range: {predictions_df['pickup_hour'].min()} to {predictions_df['pickup_hour'].max()}")
    
    # Read actuals directly from feature group
    print("Fetching actuals from feature group...")
    actuals_fg = feature_store.get_feature_group(
        name=config.FEATURE_GROUP_NAME,
        version=config.FEATURE_GROUP_VERSION
    )
    actuals_df = actuals_fg.read()
    print(f"Actuals shape: {actuals_df.shape}")
    
    if actuals_df.empty:
        print("WARNING: No actuals found in feature store!")
        return pd.DataFrame(columns=['pickup_location_id', 'predicted_demand', 'pickup_hour', 'rides'])
    
    actuals_df['pickup_hour'] = pd.to_datetime(actuals_df['pickup_hour'])
    print(f"Actuals date range: {actuals_df['pickup_hour'].min()} to {actuals_df['pickup_hour'].max()}")
    
    # Merge predictions with actuals
    monitoring_df = predictions_df.merge(
        actuals_df[['pickup_location_id', 'pickup_hour', 'rides']],
        on=['pickup_location_id', 'pickup_hour'],
        how='inner'
    )
    
    print(f"Merged shape: {monitoring_df.shape}")
    
    if monitoring_df.empty:
        print("WARNING: No matching data between predictions and actuals!")
        print("Predictions are for times where no actual ride data exists yet.")
        return pd.DataFrame(columns=['pickup_location_id', 'predicted_demand', 'pickup_hour', 'rides'])
    
    # Filter to date range
    monitoring_df = monitoring_df[monitoring_df['pickup_hour'].between(from_date, to_date)]
    
    # Remove duplicates
    monitoring_df = monitoring_df.drop_duplicates(
        subset=['pickup_location_id', 'pickup_hour'],
        keep='last'
    )
    
    print(f"Final shape after filtering: {monitoring_df.shape}")
    
    return monitoring_df