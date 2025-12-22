from datetime import datetime
from typing import Tuple

import pandas as pd

def train_test_split(df: pd.DataFrame,
                     cutoff_date: datetime,
                     target_column_name: str,
                     ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Split a DataFrame into training and test sets based on a datetime cutoff.

    Rows with a ``pickup_hour`` earlier than ``cutoff_date`` are assigned to
    the training set, while rows with a ``pickup_hour`` on or after the cutoff
    are assigned to the test set. The target column is separated from the
    feature columns in each split.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing features, the target column, and a
        ``pickup_hour`` datetime column used for splitting.
    cutoff_date : datetime
        Datetime threshold used to divide the data into training and test sets.
    target_column_name : str
        Name of the target column to be predicted.

    Returns
    -------
    X_train : pd.DataFrame
        Training feature DataFrame (all columns except the target).
    y_train : pd.Series
        Training target values.
    X_test : pd.DataFrame
        Test feature DataFrame (all columns except the target).
    y_test : pd.Series
        Test target values.

    Notes
    -----
    - The returned DataFrames have their indices reset.
    - This function performs a **time-based split**, which is suitable for
      time-series or temporally ordered data.
    """
    train_data = df[df['pickup_hour'] < cutoff_date].reset_index(drop=True)
    test_data = df[df['pickup_hour'] >= cutoff_date].reset_index(drop=True)

    X_train = train_data.drop(columns=target_column_name)
    y_train = train_data[target_column_name]
    X_test = test_data.drop(columns=target_column_name)
    y_test = test_data[target_column_name]

    return X_train, y_train, X_test, y_test

    