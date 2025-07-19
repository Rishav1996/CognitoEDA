"""
This module defines the tools available for the LangChain agents.
It includes tools for academic research (arXiv), web searches (DuckDuckGo),
and a Python REPL for code execution with a DataFrame context.
"""

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_experimental.utilities import PythonREPL
from langchain.tools import Tool

# A tool for searching and retrieving information from arXiv.
arxiv_tool = load_tools(["arxiv"])

# A tool for performing web searches using DuckDuckGo.
duckduckgo_tool = DuckDuckGoSearchResults(output_type="json")


def get_python_repl_tool_with_df(df):
    """
    Creates and returns a LangChain Tool that wraps a PythonREPL instance.
    This tool is initialized with a specific pandas DataFrame, making it
    available for code execution within the REPL.

    Args:
        df (pd.DataFrame): The pandas DataFrame to be included in the REPL's local scope.

    Returns:
        Tool: A LangChain tool configured for Python code execution with the DataFrame.
    """
    repl = PythonREPL(locals={"df": df})

    def run_python_code(code: str) -> str:
        """Executes the given Python code in the REPL environment."""
        return repl.run(code)

    return Tool(
        name="PythonREPL",
        func=run_python_code,
        description="Executes arbitrary Python code with access to the DataFrame 'df'."
    )

# A list of common tools available to the agents.
common_tools = arxiv_tool + [duckduckgo_tool]
