from utils.prompt import PROMPT_MAPPER
from utils.schema import PARSER_MAPPER
from utils.tools import common_tools, get_python_repl_tool_with_df

from langchain_core.runnables import RunnableConfig
from utils.helper import get_model, AgentState, STAGE_MAPPER, WorkflowStage


from langgraph.prebuilt import create_react_agent

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import time
import logging


MODEL_GEMINI = get_model()


def get_prompt(state: AgentState):
    """
    Get the prompt for the agent based on the current state.
    """
    task = state.task
    stage = state.stage
    metadata = state.metadata if state.metadata else {}
    statistics = state.statistics if state.statistics else {}

    if stage == WorkflowStage.METADATA_EXTRACTOR_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools)
        )
    elif stage == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            content=task
        )
    elif stage == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            metadata=metadata
        )
    elif stage == WorkflowStage.PYTHON_CODER_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            tool_list=", ".join(getattr(tool, "name", tool.__class__.__name__) for tool in common_tools),
            task=task
        )
    elif stage == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            metadata=metadata,
            statistics=statistics
        )
    elif stage == WorkflowStage.WEB_DEVELOPER_AGENT:
        return PROMPT_MAPPER[stage].format(
            output_format=PARSER_MAPPER[stage].get_format_instructions(),
            tool_list=", ".join(tool.name for tool in common_tools),
            insights=task,
            metadata=metadata,
            statistics=statistics,
            dataframe=state.df.to_json(orient="records")
        )


def llm_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a React agent for metadata extraction.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    task_list = state.task if isinstance(state.task, list) else [state.task]
    retry_method = config.get("retry_method", 10)
    stage = state.stage
    agent_retry_sleep_seconds = config.get("agent_retry_sleep_seconds", 20)

    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=get_prompt(state)
    )
    content_list = []
    for task in task_list:
        content = agent.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['messages'][-1].content
        while retry_method > 0:
            try:
                content = PARSER_MAPPER[stage].parse(content)
                content = content.output_format
                content_list.append(content)
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_retry_sleep_seconds} seconds...")
                retry_method -= 1
                time.sleep(agent_retry_sleep_seconds)
                content = agent.invoke(
                    {"messages": [{"role": "user", "content": task}]}
                )['messages'][-1].content
        if retry_method == 0:
            logging.error("Failed to parse content after multiple retries.")
            raise ValueError("Failed to parse content after multiple retries.")
    state.task = content_list[0] if len(content_list) == 1 else content_list
    state.stage = STAGE_MAPPER[stage]
    state.history = state.history + [{'task': task, 'stage': stage}]
    return state


def pandas_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a Pandas DataFrame agent for metadata extraction.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    retry_method = config.get("retry_method", 10)
    agent_retry_sleep_seconds = config.get("agent_retry_sleep_seconds", 20)
    df = state.df
    task_list = [tate.task] if isinstance(state.task, str) else " ".join(state.task)

    agent = create_pandas_dataframe_agent(
        MODEL_GEMINI,
        df,
        allow_dangerous_code=True
    )
    output_list = []
    for task in task_list:
        while retry_method > 0:
            try:
                # If you have a parser for the output, use it here
                # parsed_output = your_parser.parse(content['output'])
                # return parsed_output
                content = agent.invoke(task)
                output_list.append({"query": task, "answer": content['output']})
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_retry_sleep_seconds} seconds...")
                retry_method -= 1
                time.sleep(agent_retry_sleep_seconds)
                content = agent.invoke(task)
    state.task = output_list[0] if len(output_list) == 1 else output_list
    state.stage = STAGE_MAPPER[stage]
    state.history = state.history + [{'task': task, 'stage': stage}]
    return state


def python_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a React agent for Python REPL execution.
    Retries parsing up to `retry_method` times, sleeping between retries.
    """
    task_list = state.task if isinstance(state.task, list) else [state.task]
    retry_method = config.get("retry_method", 10)
    stage = state.stage
    agent_retry_sleep_seconds = config.get("agent_retry_sleep_seconds", 20)
    df = state.df

    tools = common_tools + [get_python_repl_tool_with_df(df)]  # Use the wrapped tool
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=tools,
        prompt=get_prompt(state)
    )
    content_list = []
    for task in task_list:
        content = agent.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['messages'][-1].content
        while retry_method > 0:
            try:
                content = PARSER_MAPPER[stage].parse(content)
                content = content.output_format
                content_list.append(content)
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_retry_sleep_seconds} seconds...")
                retry_method -= 1
                time.sleep(agent_retry_sleep_seconds)
                content = agent.invoke(
                    {"messages": [{"role": "user", "content": task}]}
                )['messages'][-1].content
        if retry_method == 0:
            logging.error("Failed to parse content after multiple retries.")
            raise ValueError("Failed to parse content after multiple retries.")
    state.task = content_list[0] if len(content_list) == 1 else content_list
    state.stage = STAGE_MAPPER[stage]
    state.history = state.history + [{'task': task, 'stage': stage}]
    return state
