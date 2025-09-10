"""Graph Agent Starting Point"""
import mlflow
from langgraph.graph import StateGraph
from dotenv import load_dotenv

load_dotenv()

from tools.agents import llm_agent, pandas_agent
from tools.helper import AgentState, ConfigSchema, NodeName


def set_mlflow():
    """
    Configures and initializes the MLflow tracking server.

    This function sets the MLflow tracking URI to a local server. It then
    attempts to set the experiment to 'CognitoEDA'. If the experiment does not
    exist, it creates it. Finally, it enables automatic logging for LangChain
    runs, which captures prompts, outputs, and other metadata.
    """
    mlflow.set_tracking_uri('http://localhost:5000')
    try:
        mlflow.set_experiment('CognitoEDA')
    except:
        mlflow.create_experiment('CognitoEDA')
    mlflow.langchain.autolog()


def create_graph(runnable_config: ConfigSchema):
    """
    Creates and compiles the agentic workflow graph using LangGraph.

    This function defines the structure of the multi-agent system. It initializes
    a state graph and adds nodes for each agent in the workflow (e.g.,
    Metadata Extractor, Python Coder, Web Developer). It then defines the
    sequence of operations by adding edges that connect these nodes in a
    specific order.

    Args:
        runnable_config (ConfigSchema): A configuration object containing run-specific
                                        parameters like UUID, temperature, etc.

    Returns:
        CompiledGraph: A compiled, runnable LangGraph agent that executes the
                       defined workflow.
    """
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
