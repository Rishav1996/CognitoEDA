"""
This module defines the tools available for the LangChain agents.
It includes tools for academic research (arXiv), web searches (DuckDuckGo),
and a Python REPL for code execution with a DataFrame context.
"""

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchResults

# A tool for searching and retrieving information from arXiv.
arxiv_tool = load_tools(["arxiv"])

# A tool for performing web searches using DuckDuckGo.
duckduckgo_tool = DuckDuckGoSearchResults(output_type="json")

# A list of common tools available to the agents.
common_tools = arxiv_tool + [duckduckgo_tool]
