from tools.prompt import PROMPT_MAPPER
from tools.schema import PARSER_MAPPER, FORMAT_MAPPER
from tools.tools import common_tools

from langchain_core.runnables import RunnableConfig
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from ast import literal_eval
import pandas as pd
from tools.helper import get_model, AgentState, get_next_stage_mapper, WorkflowStage

from langgraph.prebuilt import create_react_agent

import time


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
    prompt=get_prompt(state)

    llm_agent_obj = create_react_agent(
        model=MODEL_GEMINI,
        tools=common_tools,
        prompt=prompt,
        response_format=FORMAT_MAPPER[stage]
    )
    content_list = []
    content = llm_agent_obj.invoke(
        {"messages": [{"role": "user", "content": '\n\n'.join(task_list)}]}
    )['structured_response']
    content = content.output_format
    if isinstance(content, list):
        content_list.extend(content)
    else:
        content_list.append(content)

    state['task'] = content_list

    if stage == WorkflowStage.STRUCTURE_CREATOR_AGENT:
        state['metadata'] = state['task']
    elif stage == WorkflowStage.STATISTICS_GENERATOR_AGENT:
        state['statistics'] = state['task']
    elif stage == WorkflowStage.BUSINESS_INSIGHTS_AGENT:
        state['insights'] = state['task']

    state['stage'] = state['stage'] + [get_next_stage_mapper(state['stage'])]
    state['history'] = state['history'] + [{'task': task_list, 'stage': stage, 'prompt': prompt, 'uuid': config.get("uuid"), 'output': content_list}]
    return state


def pandas_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    task_list = state['task'] if isinstance(state['task'], list) else [state['task']]
    stage = state['stage'][-1]
    df = state['df']
    df = literal_eval(df)
    columns = list(df[0].keys())
    df = [list(i.values()) for i in df]
    df = pd.DataFrame(data=df, columns=columns)
    agent_sleep_seconds = config.get('metadata').get("agent_sleep_seconds")
    pandas_agent_obj = create_pandas_dataframe_agent(llm=MODEL_GEMINI, df=df, agent_type='tool-calling', allow_dangerous_code=True)
    content_list = []
    for task in task_list:
        content = pandas_agent_obj.invoke(task  + '\n\nNote: if unable to answer return `None`')
        content = content['output']
        if content != 'None':
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
    state['history'] = state['history'] + [{'task': task, 'stage': stage, 'uuid': config.get("uuid"), 'output': content_list}]
    return state
