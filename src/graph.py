from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph
from utils.helper import AgentState, ConfigSchema, WorkflowStage
from utils.agents import llm_agent, pandas_agent
import pandas as pd
import os
from datetime import datetime
import traceback
import uuid
import json
import mlflow


mlflow.set_tracking_uri('http://localhost:5000')

try:
    mlflow.set_experiment('CognitoEDA')
except:
    mlflow.create_experiment('CognitoEDA')

mlflow.langchain.autolog()

uuid_num = str(uuid.uuid4())

runnable_config = ConfigSchema(uuid=uuid_num, agent_sleep_seconds=30)

state = AgentState(
    task= ["The target column is `variety` and this is a `classification` use case."],
    metadata= [],
    statistics= [],
    insights= [],
    df= pd.read_csv('./data/temp.csv').to_json(orient="records"),
    stage= [WorkflowStage.METADATA_EXTRACTOR_AGENT],
    history= []
)

graph = StateGraph(AgentState, config_schema=ConfigSchema)


graph.add_node("Metadata Extractor Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Structured Generator Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Statistician Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Python Coder Agent - Pandas", pandas_agent, config_schema=runnable_config)
graph.add_node("Python Coder Agent - Statistics", pandas_agent, config_schema=runnable_config)
graph.add_node("Business Insight Agent", llm_agent, config_schema=runnable_config)
graph.add_node("Web Developer Agent", llm_agent, config_schema=runnable_config)

graph.add_edge("Metadata Extractor Agent", "Python Coder Agent - Pandas")
graph.add_edge("Python Coder Agent - Pandas", "Structured Generator Agent")
graph.add_edge("Structured Generator Agent", "Statistician Agent")
graph.add_edge("Statistician Agent", "Python Coder Agent - Statistics")
graph.add_edge("Python Coder Agent - Statistics", "Business Insight Agent")
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
        agent_name = list(stage_output.keys())[0]
        print(f'Completed Agent Flow - {agent_name}')
        if agent_name == "Web Developer Agent":
            with open('./logs/' + uuid_num + f'/index.html', 'w') as f:
                f.write(str(stage_output["Web Developer Agent"]['task'][0]))
        with open('./logs/' + uuid_num + f'/{agent_name}-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
            f.write(str(stage_output))
except:
    with open('./logs/' + uuid_num + '/error_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
        f.write(traceback.format_exc())
