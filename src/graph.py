from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph
from langchain_core.runnables.retry import RunnableRetry
import pandas as pd
import os
from datetime import datetime
import traceback
import mlflow

from tools.agents import llm_agent, pandas_agent
from tools.helper import AgentState, ConfigSchema, WorkflowStage, NodeName



# runnable_config = ConfigSchema(uuid=uuid_num, agent_sleep_seconds=30, temperature=1.0)

# state = AgentState(
#     task= ["The target column is `variety` and this is a `classification` use case."],
#     metadata= [],
#     statistics= [],
#     insights= [],
#     df= pd.read_csv("D:\\Downloads\\diabetes.csv").to_json(orient="records"),
#     stage= [WorkflowStage.METADATA_EXTRACTOR_AGENT],
#     history= []
# )

def set_mlflow():
    mlflow.set_tracking_uri('http://localhost:5000')
    try:
        mlflow.set_experiment('CognitoEDA')
    except:
        mlflow.create_experiment('CognitoEDA')
    mlflow.langchain.autolog()


def create_graph():
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


# set_mlflow()
# graph_agent = create_graph()

# with open('./data/graph.png', 'wb') as f:
#     f.write(graph_agent.get_graph().draw_mermaid_png())


# if not os.path.exists(f'./logs/{uuid_num}'):
#     os.mkdir(f'./logs/{uuid_num}')

# try:
#     for stage_output in graph_agent.stream(state, runnable_config):
#         agent_name = list(stage_output.keys())[0]
#         print(f'Completed Agent Flow - {agent_name}')
#         if agent_name == NodeName.WEB_DEVELOPER_AGENT.value:
#             with open('./logs/' + uuid_num + f'/index.html', 'w') as f:
#                 f.write(str(stage_output[NodeName.WEB_DEVELOPER_AGENT.value]['task'][0]))
#         with open('./logs/' + uuid_num + f'/{agent_name}-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
#             f.write(str(stage_output).replace('\n', '\\n'))
# except:
#     with open('./logs/' + uuid_num + '/error_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
#         f.write(traceback.format_exc())
