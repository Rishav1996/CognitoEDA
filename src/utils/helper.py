from enum import Enum
from typing import Optional
from typing_extensions import TypedDict, Literal
from langchain.chat_models import init_chat_model
import pandas as pd
from langgraph.graph import END


class ModelClasses(Enum):
    """
    Enum for different model classes.
    """
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    TIME_SERIES = "time_series"
    ANOMALY_DETECTION = "anomaly_detection"

class WorkflowStage(Enum):
    """
    Enum for different workflow stages.
    """
    METADATA_EXTRACTOR_AGENT = "metadata_extractor_agent"
    STRUCTURE_CREATOR_AGENT = "structure_creator_agent"
    STATISTICS_GENERATOR_AGENT = "statistics_generator_agent"
    PANDAS_AGENT = "pandas_agent"
    PYTHON_CODER_AGENT = "python_coder_agent"
    BUSINESS_INSIGHTS_AGENT = "business_insights_agent"
    WEB_DEVELOPER_AGENT = "web_developer_agent"

class AgentState(TypedDict):
    """
    State for the agent graph.
    """
    task: list | str
    metadata: Optional[dict] = None
    statistics: Optional[dict] = None
    df: pd.DataFrame
    stage: WorkflowStage
    history: list = []

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

STAGE_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: WorkflowStage.PANDAS_AGENT,
    WorkflowStage.PANDAS_AGENT: WorkflowStage.STRUCTURE_CREATOR_AGENT,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: WorkflowStage.STATISTICS_GENERATOR_AGENT,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: WorkflowStage.PYTHON_CODER_AGENT,
    WorkflowStage.PYTHON_CODER_AGENT: WorkflowStage.BUSINESS_INSIGHTS_AGENT,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: WorkflowStage.WEB_DEVELOPER_AGENT
}
