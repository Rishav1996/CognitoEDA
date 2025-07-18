from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchResults


arxiv_tool = load_tools(["arxiv"])
duckduckgo_tool = DuckDuckGoSearchResults(output_type="json")

metadata_extractor_tools = arxiv_tool + [duckduckgo_tool]
