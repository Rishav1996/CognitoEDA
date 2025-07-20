from utils.prompt import PROMPT_MAPPER
from utils.schema import PARSER_MAPPER
from utils.tools import common_tools, get_python_repl_tool_with_df

from langchain_core.runnables import RunnableConfig
from utils.helper import get_model, AgentState, STAGE_MAPPER, WorkflowStage


from langgraph.prebuilt import create_react_agent

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import time
import logging
import pandas as pd


MODEL_GEMINI = get_model()


def get_prompt(state: AgentState):
    """
    Get the prompt for the agent based on the current state.
    """
    task = state['task']
    stage = state['stage']
    metadata = state['metadata'] if state['metadata'] else {}
    insights = state['insights'] if state['insights'] else {}
    statistics = state['statistics'] if state['statistics'] else {}
    df = state['df']

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
            task=task,
            dataframe=df
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
            insights=insights,
            metadata=metadata,
            statistics=statistics
        )


def llm_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a React agent for metadata extraction.
    Retries parsing up to `agent_retry_limit` times, sleeping between retries.
    """
    task_list = state['task'] if isinstance(state['task'], list) else [state['task']]
    stage = state['stage']
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")

    llm_agent_obj = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=get_prompt(state)
    )
    content_list = []
    for task in task_list:
        agent_retry_limit = config.get('metadata').get("agent_retry_limit")
        content = llm_agent_obj.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['messages'][-1].content
        while agent_retry_limit > 0:
            try:
                content = PARSER_MAPPER[stage].parse(content)
                content = content.output_format
                content_list.append(content)
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_sleep_seconds} seconds...")
                agent_retry_limit -= 1
                time.sleep(agent_sleep_seconds)
                content = llm_agent_obj.invoke(
                    {"messages": [{"role": "user", "content": task}]}
                )['messages'][-1].content
        if agent_retry_limit == 0:
            logging.error("Failed to parse content after multiple retries.")
            raise ValueError("Failed to parse content after multiple retries.")
    state['task'] = content_list[0] if len(content_list) == 1 else content_list
    state['stage'] = STAGE_MAPPER[stage]
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'uuid': config.get("uuid"), 'output': content_list}]

    if state['stage'] == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    if state['stage'] == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    if state['stage'] == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']
    return state


def pandas_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a Pandas DataFrame agent for metadata extraction.
    Retries parsing up to `agent_retry_limit` times, sleeping between retries.
    """
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")
    df = pd.read_json(state['df'])
    stage = state['stage']
    task_list = state['task'] if isinstance(state['task'], list) else [state['task']]

    pandas_agent_obj = create_pandas_dataframe_agent(
        MODEL_GEMINI,
        df=df,
        allow_dangerous_code=True,
        agent_type="tool-calling",
        max_iterations=3,
    )
    output_list = []
    for task in task_list:
        agent_retry_limit = config.get('metadata').get("agent_retry_limit")
        while agent_retry_limit > 0:
            try:
                content = pandas_agent_obj.invoke(task)
                output_list.append({"query": task, "answer": content['output']})
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_sleep_seconds} seconds...")
                agent_retry_limit -= 1
                time.sleep(agent_sleep_seconds)
    state['task'] = output_list[0]['answer'] if len(output_list) == 1 else [i['answer'] for i in output_list]
    state['stage'] = STAGE_MAPPER[stage]
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'uuid': config.get("uuid"), 'output': output_list}]
    if state['stage'] == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    if state['stage'] == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    if state['stage'] == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']
    return state


def python_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a React agent for Python REPL execution.
    Retries parsing up to `agent_retry_limit` times, sleeping between retries.
    """
    task_list = state['task'] if isinstance(state['task'], list) else [state['task']]
    stage = state['stage']
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")
    df = state['df']

    tools = common_tools + [get_python_repl_tool_with_df(df)]  # Use the wrapped tool
    python_agent_obj = create_react_agent(
        model=MODEL_GEMINI,
        tools=tools,
        prompt=get_prompt(state)
    )
    content_list = []
    for task in task_list:
        agent_retry_limit = config.get('metadata').get("agent_retry_limit")
        content = python_agent_obj.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['messages'][-1].content
        while agent_retry_limit > 0:
            try:
                content = PARSER_MAPPER[stage].parse(content)
                content = content.output_format
                content_list.append(content)
                break
            except Exception as e:
                logging.warning(f"Parsing failed: {e}. Retrying after {agent_sleep_seconds} seconds...")
                agent_retry_limit -= 1
                time.sleep(agent_sleep_seconds)
                content = python_agent_obj.invoke(
                    {"messages": [{"role": "user", "content": task}]}
                )['messages'][-1].content
        if agent_retry_limit == 0:
            logging.error("Failed to parse content after multiple retries.")
            raise ValueError("Failed to parse content after multiple retries.")
    state['task'] = content_list[0] if len(content_list) == 1 else content_list
    state['stage'] = STAGE_MAPPER[stage]
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'uuid': config.get("uuid"), 'output': content_list}]
    if state['stage'] == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    if state['stage'] == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    if state['stage'] == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']
    return state
