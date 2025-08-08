from enum import Enum


class ModelClasses(Enum):
    """
    Enum for different model classes.
    """
    CLASSIFICATION = "Classification"
    REGRESSION = "Regression"
    CLUSTERING = "Clustering"
    TIME_SERIES = "Time Series"
    ANOMALY_DETECTION = "Anomaly Detection"
