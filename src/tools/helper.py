from enum import Enum
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import END


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


WORKFLOW_SEQUENCE = [
    WorkflowStage.METADATA_EXTRACTOR_AGENT,
    WorkflowStage.PYTHON_CODER_AGENT,
    WorkflowStage.STRUCTURE_CREATOR_AGENT,
    WorkflowStage.STATISTICS_GENERATOR_AGENT,
    WorkflowStage.PYTHON_CODER_AGENT,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT,
    WorkflowStage.WEB_DEVELOPER_AGENT
]

def get_model(model:str ="models/gemini-2.5-flash", model_provider:str ="google_genai", temperature: float = 1.0):
    """
    Get the model for the agent.
    """
    return init_chat_model(
        model=model,
        model_provider=model_provider,
        temperature=temperature
    )

def get_next_stage_mapper(history_stage: list[WorkflowStage]) -> WorkflowStage:
    """
    Get the next state for the agent.
    """
    for index in range(len(WORKFLOW_SEQUENCE)):
        if ''.join(map(str, WORKFLOW_SEQUENCE[:index])) == ''.join(map(str, history_stage)):
            return WORKFLOW_SEQUENCE[index]
    return END
