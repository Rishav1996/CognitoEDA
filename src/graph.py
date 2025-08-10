from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph
from langchain_core.runnables.retry import RunnableRetry

import traceback
import mlflow

from tools.agents import llm_agent, pandas_agent
from tools.helper import AgentState, ConfigSchema, WorkflowStage, NodeName


def set_mlflow():
    mlflow.set_tracking_uri('http://localhost:5000')
    try:
        mlflow.set_experiment('CognitoEDA')
    except:
        mlflow.create_experiment('CognitoEDA')
    mlflow.langchain.autolog()


def create_graph(runnable_config: ConfigSchema):
    graph = StateGraph(AgentState, config_schema=ConfigSchema)
    graph.add_node(NodeName.METADATA_EXTRACTOR_AGENT.value, llm_agent, config_schema=runnable_config)
    graph.add_node(NodeName.STRUCTURE_CREATOR_AGENT.value, llm_agent, config_schema=runnable_config)
    graph.add_node(NodeName.STATISTICS_GENERATOR_AGENT.value, llm_agent, config_schema=runnable_config)
    graph.add_node(NodeName.PYTHON_PANDAS_CODER_AGENT.value, pandas_agent, config_schema=runnable_config)
    graph.add_node(NodeName.PYTHON_STATISTICS_CODER_AGENT.value, pandas_agent, config_schema=runnable_config)
    graph.add_node(NodeName.BUSINESS_INSIGHTS_AGENT.value, llm_agent, config_schema=runnable_config)
    graph.add_node(NodeName.WEB_DEVELOPER_AGENT.value, llm_agent, config_schema=runnable_config)

    graph.add_edge(NodeName.METADATA_EXTRACTOR_AGENT.value, NodeName.PYTHON_PANDAS_CODER_AGENT.value)
    graph.add_edge(NodeName.PYTHON_PANDAS_CODER_AGENT.value, NodeName.STRUCTURE_CREATOR_AGENT.value)
    graph.add_edge(NodeName.STRUCTURE_CREATOR_AGENT.value, NodeName.STATISTICS_GENERATOR_AGENT.value)
    graph.add_edge(NodeName.STATISTICS_GENERATOR_AGENT.value, NodeName.PYTHON_STATISTICS_CODER_AGENT.value)
    graph.add_edge(NodeName.PYTHON_STATISTICS_CODER_AGENT.value, NodeName.BUSINESS_INSIGHTS_AGENT.value)
    graph.add_edge(NodeName.BUSINESS_INSIGHTS_AGENT.value, NodeName.WEB_DEVELOPER_AGENT.value)

    graph.set_entry_point(NodeName.METADATA_EXTRACTOR_AGENT.value)
    graph.set_finish_point(NodeName.WEB_DEVELOPER_AGENT.value)

    graph_agent = graph.compile()
    return graph_agent
