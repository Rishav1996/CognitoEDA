from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from utils.helper import AgentState, ConfigSchema, WorkflowStage
from utils.agents import llm_agent, pandas_agent, python_agent
import pandas as pd
import os
from datetime import datetime
import traceback
import uuid
import json


uuid_num = str(uuid.uuid4())

runnable_config = ConfigSchema(uuid=uuid_num, agent_retry_limit=2, agent_sleep_seconds=60)

state = AgentState(
    task= "Suggest all possible EDA considering the target column is `variety` and this is a `classification` use case. Example: datatypes of columns, null values and many more",
    metadata= [],
    statistics= [],
    insights= [],
    df= pd.read_csv('./data/temp.csv').to_json(),
    stage= WorkflowStage.METADATA_EXTRACTOR_AGENT,
    history= []
)

graph = StateGraph(AgentState, config_schema=ConfigSchema)


graph.add_node("Metadata Extractor Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Pandas Agent", pandas_agent, config_schema=runnable_config)
graph.add_node("Structured Generator Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Statistician Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Python Coder Agent", python_agent, config_schema=runnable_config)
graph.add_node("Business Insight Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Web Developer Agent", llm_agent, config_schema=runnable_config)

graph.add_edge("Metadata Extractor Agent", "Pandas Agent")
graph.add_edge("Pandas Agent", "Structured Generator Agent")
graph.add_edge("Structured Generator Agent", "Statistician Agent")
graph.add_edge("Statistician Agent", "Python Coder Agent")
graph.add_edge("Python Coder Agent", "Business Insight Agent")
graph.add_edge("Business Insight Agent", "Web Developer Agent")

graph.set_entry_point("Metadata Extractor Agent")
graph.set_finish_point("Web Developer Agent")

graph_agent = graph.compile()

with open('./data/graph.png', 'wb') as f:
    f.write(graph_agent.get_graph().draw_mermaid_png())


if not os.path.exists(f'./logs/{uuid_num}'):
    os.mkdir(f'./logs/{uuid_num}')

try:
    for stage_output in graph_agent.stream(state, runnable_config):
        with open('./logs/' + uuid_num + '/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
            f.write(str(stage_output))
except:
    with open('./logs/' + uuid_num + '/error_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
        f.write(traceback.format_exc())
