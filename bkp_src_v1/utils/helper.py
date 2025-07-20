from enum import Enum
from typing import Optional
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
import pandas as pd

from utils.helper import ModelClasses


class ModelClasses(Enum):
    """
    Enum for different model classes.
    """
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    TIME_SERIES = "time_series"
    ANOMALY_DETECTION = "anomaly_detection"

class AgentState(TypedDict):
    """
    State for the agent graph.
    """
    task: list | str
    df: pd.DataFrame
    type_of_modelling: str
    model_class: ModelClasses
    target_column: Optional[str] = None
    n_steps: int = 10
    history: list

class ConfigSchema(TypedDict):
    """
    Configuration for the agent graph.
    """
    agent_retry_limit: int = 3
    agent_sleep_seconds: int = 20


def get_model(temperature: float = 1.0):
    """
    Get the model for the agent.
    """
    return init_chat_model(
        model="models/gemini-2.5-flash",
        model_provider="google_genai",
        temperature=temperature
    )