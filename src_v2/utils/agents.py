from utils.prompt import *
from utils.tools import *
from langchain_core.runnables import RunnableConfig
from utils.helper import get_model, AgentState


from langgraph.prebuilt import create_react_agent

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import time
import logging

# Sleep duration (in seconds) between agent retries
AGENT_RETRY_SLEEP_SECONDS = 20
MODEL_GEMINI = get_model()

def agent_metadata_extractor(state: AgentState, config: RunnableConfig) -> MetadataExtractorOutputFormatSchema:
    """
    Create a React agent for metadata extraction.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    task = state.task
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=METADATA_EXTRACTOR_PROMPT.format(
            output_format=metadata_parser.get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools)
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": task}]}
    )['messages'][-1].content
    while retry_method > 0:
        try:
            content = metadata_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": task}]}
            )['messages'][-1].content
    state = AgentState(task=content, **state)
    return state


def agent_pandas_dataframe_extractor(df, message, retry_method=10):
    """
    Create a Pandas DataFrame agent for metadata extraction.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    agent = create_pandas_dataframe_agent(
        MODEL_GEMINI,
        df,
        allow_dangerous_code=True
    )
    while retry_method > 0:
        try:
            # If you have a parser for the output, use it here
            # parsed_output = your_parser.parse(content['output'])
            # return parsed_output
            content = agent.invoke(message)
            return {"query": message, "answer": content['output']}
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(message)
    return {"query": message, "answer": content['output']}


def agent_metadata_to_structured_file(question_answer_obj, retry_method=10):
    """
    Convert the question-answer dictionary to a structured file format.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=[],
        prompt=STRUCTURED_FILE_PROMPT.format(
            output_format=structured_file_parser.get_format_instructions(),
            content=question_answer_obj
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Generate humanly readable structured output"}]}
    )['messages'][-1].content
    while retry_method > 0:
        try:
            content = structured_file_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": "Generate humanly readable structured output"}]}
            )['messages'][-1].content
    return content


def agent_statistics_extractor(retry_method=10) -> StatisticsExtractorOutputFormatSchema:
    """
    Create a React agent for statistics extraction.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    with open("./data/metadata.txt", "r") as file:
        metadata = file.read()

    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=STATISTICS_EXTRACTOR_PROMPT.format(
            output_format=statistics_parser.get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            metadata=metadata
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Generate statistical extraction steps"}]}
    )['messages'][-1].content
    logging.info(content)
    while retry_method > 0:
        try:
            content = statistics_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": "Generate statistical extraction steps"}]}
            )['messages'][-1].content
    return content


def agent_python_repl(df, task, retry_method=10) -> str:
    """
    Create a React agent for Python REPL execution.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    tools = common_tools + [get_python_repl_tool_with_df(df)]  # Use the wrapped tool
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=tools,
        prompt=PYTHON_REPL_PROMPT.format(
            output_format=python_repl_parser.get_format_instructions(),
            tool_list=", ".join(getattr(tool, "name", tool.__class__.__name__) for tool in tools),
            task=task
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Create a Python function for the task and execute it"}]}
    )['messages'][-1].content
    logging.info(content)
    while retry_method > 0:
        try:
            content = python_repl_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": "Create a Python function for the task and execute it"}]}
            )['messages'][-1].content
    return content


def agent_business_insight_generator(df, retry_method=10) -> str:
    """
    Create a React agent for business insight generation.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    with open("./data/metadata.txt", "r") as file:
        metadata = file.read()
    with open('./data/statistics.txt', "r") as file:
        statistics = file.read()

    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=BUSINESS_ANALYTICS_PROMPT.format(
            output_format=business_analytics_parser.get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            metadata=metadata,
            statistics=statistics
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Generate business insights"}]}
    )['messages'][-1].content
    while retry_method > 0:
        try:
            content = business_analytics_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": "Generate business insights"}]}
            )['messages'][-1].content
    return content


def agent_html_insight_generator(df, insights, retry_method=10) -> str:
    """
    Create a React agent for HTML insight generation.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    with open("./data/metadata.txt", "r") as file:
        metadata = file.read()
    with open('./data/statistics.txt', "r") as file:
        statistics = file.read()
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=HTML_INSIGHT_GENERATOR_PROMPT.format(
            output_format=html_insight_parser.get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            insights=insights,
            metadata=metadata,
            statistics=statistics,
            dataframe=df.to_json(orient="records")
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Convert existing insights into a Web Page that support charts and images"}]}
    )['messages'][-1].content
    while retry_method > 0:
        try:
            content = html_insight_parser.parse(content)
            return content
        except Exception as e:
            logging.warning(f"Parsing failed: {e}. Retrying after {AGENT_RETRY_SLEEP_SECONDS} seconds...")
            retry_method -= 1
            time.sleep(AGENT_RETRY_SLEEP_SECONDS)
            content = agent.invoke(
                {"messages": [{"role": "user", "content": "Convert existing insights into a Web page that support charts and images"}]}
            )['messages'][-1].content
    return content
