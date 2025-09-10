"""Helper Functions"""
from enum import Enum

from langchain.chat_models import init_chat_model
from langgraph.graph import END
from typing_extensions import TypedDict


class WorkflowStage(Enum):
    """
    Enum for different workflow stages.
    """
    METADATA_EXTRACTOR_AGENT = "metadata_extractor_agent"
    STRUCTURE_CREATOR_AGENT = "structure_creator_agent"
    STATISTICS_GENERATOR_AGENT = "statistics_generator_agent"
    PYTHON_CODER_AGENT = "python_coder_agent"
    BUSINESS_INSIGHTS_AGENT = "business_insights_agent"
    WEB_DEVELOPER_AGENT = "web_developer_agent"

class NodeName(Enum):
    """
    Enum for node names.
    """
    METADATA_EXTRACTOR_AGENT = "Metadata Extractor Agent"
    STRUCTURE_CREATOR_AGENT = "Structured Generator Agent"
    STATISTICS_GENERATOR_AGENT = "Statistician Agent"
    PYTHON_PANDAS_CODER_AGENT = "Python Coder Agent - Pandas"
    PYTHON_STATISTICS_CODER_AGENT = "Python Coder Agent - Statistics"
    BUSINESS_INSIGHTS_AGENT = "Business Insight Agent"
    WEB_DEVELOPER_AGENT = "Web Developer Agent"

class AgentState(TypedDict):
    """
    State for the agent graph.
    """
    task: list
    metadata: list
    statistics: list
    insights: list
    df: list
    stage: list[WorkflowStage]
    history: list


class ConfigSchema(TypedDict):
    """
    Configuration for the agent graph.
    """
    uuid: str
    agent_sleep_seconds: int
    temperature: float


WORKFLOW_SEQUENCE = [
    WorkflowStage.METADATA_EXTRACTOR_AGENT,
    WorkflowStage.PYTHON_CODER_AGENT,
    WorkflowStage.STRUCTURE_CREATOR_AGENT,
    WorkflowStage.STATISTICS_GENERATOR_AGENT,
    WorkflowStage.PYTHON_CODER_AGENT,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT,
    WorkflowStage.WEB_DEVELOPER_AGENT
]

def get_model(temperature: float = 1.0):
    """
    Initializes and returns a chat model instance from a specified provider.

    This function configures and provides an LLM instance, specifically a
    Google GenAI model, with a given temperature setting.

    Args:
        temperature (float, optional): The temperature for the model's sampling,
                                       controlling randomness. Defaults to 1.0.

    Returns:
        An initialized chat model instance.
    """
    return init_chat_model(
        model="models/gemini-2.5-pro",
        model_provider="google_genai",
        temperature=temperature
    )

def get_next_stage_mapper(history_stage: list[WorkflowStage]) -> WorkflowStage:
    """
    Determines the next workflow stage based on the history of completed stages.

    It compares the sequence of stages in `history_stage` against the predefined
    `WORKFLOW_SEQUENCE` to find the next stage to be executed. If the entire
    workflow has been completed, it returns the `END` marker.

    Args:
        history_stage (list[WorkflowStage]): A list of workflow stages that have
                                             already been executed.

    Returns:
        WorkflowStage | object: The next `WorkflowStage` enum member to execute, or
                                `END` if the sequence is complete.
    """
    for index, _ in enumerate(WORKFLOW_SEQUENCE):
        if ''.join(map(str, WORKFLOW_SEQUENCE[:index])) == ''.join(map(str, history_stage)):
            return WORKFLOW_SEQUENCE[index]
    return END
