from utils.prompt import PROMPT_MAPPER
from utils.schema import PARSER_MAPPER, FORMAT_MAPPER
from utils.tools import get_python_repl_tool_with_df, common_tools

from langchain_core.runnables import RunnableConfig
from utils.helper import get_model, AgentState, get_next_stage_mapper, WorkflowStage


from langgraph.prebuilt import create_react_agent

import time
import logging


MODEL_GEMINI = get_model()


def get_prompt(state: AgentState):
    """
    Get the prompt for the agent based on the current state.
    """
    task = state['task']
    stage = state['stage'][-1]
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
            tool_list=", ".join(getattr(tool, "name", tool.__class__.__name__) for tool in common_tools + [get_python_repl_tool_with_df(df)]),
            task=task,
            metadata=metadata
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
    stage = state['stage'][-1]
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")
    prompt=get_prompt(state)

    llm_agent_obj = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=prompt,
        response_format=FORMAT_MAPPER[stage]
    )
    content_list = []
    for task in task_list:
        content = llm_agent_obj.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['structured_response']
        content = content.output_format
        if isinstance(content, list):
            content_list.extend(content)
        else:
            content_list.append(content)
        time.sleep(agent_sleep_seconds)

    state['task'] = content_list

    if stage == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    elif stage == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    elif stage == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']

    state['stage'] = state['stage'] + [get_next_stage_mapper(state['stage'])]
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'prompt': prompt, 'uuid': config.get("uuid"), 'output': content_list}]
    return state


def python_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Create a React agent for Python REPL execution.
    Retries parsing up to `agent_retry_limit` times, sleeping between retries.
    """
    task_list = state['task'] if isinstance(state['task'], list) else [state['task']]
    stage = state['stage'][-1]
    df = state['df']
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")
    prompt=get_prompt(state)

    tools = common_tools + [get_python_repl_tool_with_df(df)]  # Use the wrapped tool
    python_agent_obj = create_react_agent(
        model=MODEL_GEMINI,
        tools=tools,
        prompt=prompt,
        response_format=FORMAT_MAPPER[stage]
    )
    content_list = []
    for task in task_list:
        content = python_agent_obj.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )['structured_response']
        content = content.output_format
        if isinstance(content, list):
            content_list.extend(content)
        else:
            content_list.append(content)
        time.sleep(agent_sleep_seconds)

    state['task'] = content_list

    if stage == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    elif stage == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    elif stage == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']

    state['stage'] = state['stage'] + [get_next_stage_mapper(state['stage'])]
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'prompt': prompt, 'uuid': config.get("uuid"), 'output': content_list}]
    return state
