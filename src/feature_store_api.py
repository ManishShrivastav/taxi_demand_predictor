from typing import Optional
import hsfs
import hopsworks

import src.config as config

def get_feature_store() -> hsfs.feature_store.FeatureStore:
    """
    Connects to Hopsworks and returns a pointer to the feature store
    
    Returns:
        hsfs.feature_store.FeatureStore: pointer to the feature store
    """
    project = hopsworks.login(
        project=config.HOPSWORKS_PROJECT_NAME,
        api_key_value=config.HOPSWORKS_API_KEY
    )
    return project.get_feature_store()

def get_feature_group(
        name: str,
        version: Optional[int] = 1
) -> hsfs.feature_group.FeatureGroup:
    """
    Connects to the feature store and returns a pointer to the given
    feature group `name`
    
    Args:
        name (str): name of the feature group
        version (Optional[int], optional): _description_. Defaults to 1
        
    Returns:
        hsfs.feature_group.FeatureGroup
    """
    return get_feature_store().get_feature_group(
        name=name,
        version=version
    )

def get_or_create_feature_group(
    name: str,
    version: int = 1,
    description: str = "",
    primary_key: list = None,
    event_time: str = None
):
    """
    Gets or creates a feature group in the feature store.
    
    Args:
        name (str): Name of the feature group
        version (int): Version of the feature group (default: 1)
        description (str): Description of the feature group
        primary_key (list): List of column names to use as primary key
        event_time (str): Name of the column to use as event time
    
    Returns:
        FeatureGroup: The feature group instance
    """
    feature_store = get_feature_store()
    return feature_store.get_or_create_feature_group(
        name=name,
        version=version,
        description=description,
        primary_key=primary_key or [],
        event_time=event_time
    )


def get_feature_view(name: str, version: int = 1):
    """
    Returns a feature view from the feature store.
    
    Args:
        name (str): Name of the feature view
        version (int): Version of the feature view (default: 1)
    
    Returns:
        FeatureView: The feature view instance
    """
    feature_store = get_feature_store()
    return feature_store.get_feature_view(
        name=name,
        version=version
    )