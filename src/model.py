import pandas as pd
import lightgbm as lgb

from typing import Optional
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline, Pipeline


def average_rides_last_4_weeks(X: pd.DataFrame) -> pd.DataFrame:
    """
    Adds one column with the average rides from
        - 7 days ago
        - 14 days ago
        - 21 days ago
        - 28 days ago
    """
    X['average_rides_last_4_weeks'] = 0.25 * (
        X[f'rides_previous_{24 * 7}_hour'] + 
        X[f'rides_previous_{24 * 7 * 2}_hour'] + 
        X[f'rides_previous_{24 * 7 * 3}_hour'] + 
        X[f'rides_previous_{24 * 7 * 4}_hour'])
    
    return X

def get_pipeline(**hyperparams) -> Pipeline:

    # sklearn transform
    add_feature_average_rides_last_4_weeks = FunctionTransformer(
    average_rides_last_4_weeks, validate=False
    )

    # sklearn transform
    add_temporal_features = TemporalFeaturesEngineer()

    # sklearn pipeline
    pipeline = make_pipeline(add_feature_average_rides_last_4_weeks, 
                             add_temporal_features, 
                             lgb.LGBMRegressor(**hyperparams)
                             )
    
    return pipeline


class TemporalFeaturesEngineer(BaseEstimator, TransformerMixin):
    def fit(
        self,
        X: pd.DataFrame,
        y: Optional[pd.Series] = None
    ) -> "TemporalFeaturesEngineer":
        return self
    
    def transform(
        self,
        X: pd.DataFrame
    ) -> pd.DataFrame:
        if 'pickup_hour' not in X.columns:
            raise KeyError("'pickup_hour' column is required")

        X_ = X.copy()

        # Ensure datetime dtype
        X_['pickup_hour'] = pd.to_datetime(X_['pickup_hour'])

        # Generate numeric features
        X_['hour'] = X_['pickup_hour'].dt.hour
        X_['day_of_week'] = X_['pickup_hour'].dt.dayofweek

        return X_.drop(columns=['pickup_hour'])
    
