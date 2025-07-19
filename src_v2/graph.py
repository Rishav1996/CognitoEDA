from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from utils.helper import AgentState, ConfigSchema
from utils.agents import llm_agent, pandas_agent, python_agent

graph = StateGraph(AgentState, config_schema=ConfigSchema)


graph.add_node("Metadata Extractor Agent", llm_agent)
graph.add_node("Pandas Agent", pandas_agent)
graph.add_node("Structured Generator Agent", llm_agent)
graph.add_node("Statistician Agent", llm_agent)
graph.add_node("Python Coder Agent", python_agent)
graph.add_node("Business Insight Agent", llm_agent)
graph.add_node("Web Developer Agent", llm_agent)

graph.add_edge("Metadata Extractor Agent", "Pandas Agent")
graph.add_edge("Pandas Agent", "Structured Generator Agent")
graph.add_edge("Structured Generator Agent", "Statistician Agent")
graph.add_edge("Statistician Agent", "Python Coder Agent")
graph.add_edge("Python Coder Agent", "Business Insight Agent")
graph.add_edge("Business Insight Agent", "Web Developer Agent")

graph.set_entry_point("Metadata Extractor Agent")
graph.set_finish_point("Web Developer Agent")

graph_agent = graph.compile()

with open('mermaid_graph.png', 'wb') as f:
    f.write(graph_agent.get_graph().draw_mermaid_png())

