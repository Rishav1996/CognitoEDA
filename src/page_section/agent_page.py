"""Agents Dashboard"""
import os
import traceback
import uuid
from copy import copy
from datetime import datetime

import pandas as pd
import streamlit as st

from graph import create_graph
from tools.helper import AgentState, ConfigSchema, NodeName, WorkflowStage
from utils.helper import ModelClasses


def trigger_agent_func():
    """
    Triggers the agentic workflow as a generator function.

    This function orchestrates the execution of a sequence of agents defined in a graph.
    It first checks if the configuration has been saved. It then initializes the agent state
    and streams through the agent graph, executing each agent in sequence.

    Yields:
        str: The name of the agent stage that has just completed.
             Yields "CONFIG_NOT_SAVED" if the configuration is not saved.
             Yields "ERROR" if an exception occurs during the agent run.
    """
    if st.session_state["configuration"]["uuid"] is None:
        yield "CONFIG_NOT_SAVED"
    if os.path.exists(f'./logs/{st.session_state["configuration"]["uuid"]}') is False:
        yield "CONFIG_NOT_SAVED"
    st.toast(f"Your Agent Run ID : {st.session_state['configuration']['uuid']}")
    runnable_config = ConfigSchema(uuid=st.session_state['configuration']['uuid'],
                                   agent_sleep_seconds=st.session_state['configuration']['agent_sleep_seconds'],
                                   temperature=st.session_state['configuration']['temperature'])

    state = AgentState(
        task= [f"The target column is `{st.session_state['configuration']['target_column']}` and this is a `{st.session_state['configuration']['problem_type']}` use case."],
        metadata= [],
        statistics= [],
        insights= [],
        df= st.session_state['configuration']['data_table'].to_json(orient="records"),
        stage= [WorkflowStage.METADATA_EXTRACTOR_AGENT],
        history= []
    )
    graph_agent = create_graph(runnable_config)
    try:
        for stage_output in graph_agent.stream(state, runnable_config):
            agent_name = list(stage_output.keys())[0]
            if agent_name == NodeName.WEB_DEVELOPER_AGENT.value:
                with open('./logs/' + st.session_state['configuration']['uuid'] + '/index.html', 'w') as f:
                    f.write(str(stage_output[NodeName.WEB_DEVELOPER_AGENT.value]['task'][0]))
            with open('./logs/' + st.session_state['configuration']['uuid'] + f'/{agent_name}-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
                f.write(str(stage_output).replace('\n', '\\n'))
            yield agent_name
    except Exception:
        with open('./logs/' + st.session_state['configuration']['uuid'] + '/error_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'w') as f:
            f.write(traceback.format_exc())
        yield 'ERROR'


def save_config_func():
    """
    Saves the current agent and data configuration to disk.

    A unique UUID is generated for the run and a corresponding directory is created
    under './logs/'. The configuration from `st.session_state` is saved as 'config.json',
    and the uploaded dataset is saved as 'data.csv' inside this directory.
    A success toast message is displayed upon completion.
    """
    st.session_state["configuration"]["uuid"] = str(uuid.uuid4())
    if not os.path.exists(f'./logs/{st.session_state["configuration"]["uuid"]}'):
        os.mkdir(f'./logs/{st.session_state["configuration"]["uuid"]}')
    config = copy(st.session_state['configuration'])
    data_table = config.pop('data_table')
    with open(f'./logs/{st.session_state["configuration"]["uuid"]}/config.json', 'w') as f:
        f.write(str(config))
    data_table.to_csv(f'./logs/{st.session_state["configuration"]["uuid"]}/data.csv', index=False)
    st.toast("Config & Data saved successfully")


def show():
    """
    Displays the main "Agentic Workflow" page in the Streamlit application.

    This function sets up the user interface for configuring the agent and the dataset,
    triggering the agentic workflow, and monitoring its progress. It includes
    input fields for agent parameters, a file uploader for the dataset, and
    select boxes for problem type and target column. It also manages the
    execution of the agent in the background and displays real-time status updates,
    finally providing a download link for the generated HTML report.
    """
    st.set_page_config(layout="wide")
    st.title("Agentic Workflow")

    with st.expander("Agent & Data Configuration", expanded=True):
        agent_config_col, data_config_col = st.columns(2)
        with agent_config_col:
            st.text("Agent Configuration")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state["configuration"]["agent_sleep_seconds"] = st.number_input("Agent Sleep Seconds",
                                                                                            min_value=10,
                                                                                            step=10,
                                                                                            value=30)
            with col2:
                st.session_state["configuration"]["temperature"] = st.number_input("Temperature", min_value=0.0, max_value=1.0, step=0.1)

        with data_config_col:
            st.text("Dataset Configuration")
            file_upload = st.file_uploader("Upload CSV Dataset", type=['csv'])
            if file_upload is not None:
                st.session_state["configuration"]["data_table"] = pd.read_csv(file_upload)
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state["configuration"]["problem_type"] = st.selectbox("Problem Type",
                                                                                     options=[val.value for _, val in ModelClasses.__members__.items()])
                with col2:
                    st.session_state["configuration"]["target_column"] = st.selectbox("Select Target Column",
                                                                                       options=st.session_state["configuration"]["data_table"].columns)
        if st.session_state["configuration"]["problem_type"] is not None and st.session_state["configuration"]["target_column"] is not None and st.session_state["configuration"]["data_table"].empty is False:
            _ , save_config_button, trigger_agent_button, _ = st.columns(4)
            with save_config_button:
                if st.button("Save Config", width="stretch"):
                    save_config_func()
            with trigger_agent_button:
                if st.button("Trigger Agent", width="stretch"):
                    if st.session_state['configuration']['status'] == "Initiating Agent .....":
                        st.session_state['configuration']['background_task'] = trigger_agent_func()
                        st.session_state['configuration']['status'] = "Agent is running ....."
                        st.session_state['configuration']['stages'] = []
                        st.rerun()
    if st.session_state['configuration']['background_task'] is not None:
        with st.container(height="stretch"):
            st.text("Agent Status Dashboard")
            if st.session_state['configuration']['background_task'] and st.session_state['configuration']['status'] == "Agent is running .....":
                with st.status(st.session_state['configuration']['status'], expanded=True) as status_box:
                    try:
                        lapsed_time = datetime.now()
                        total_time = 0
                        for msg in st.session_state['configuration']['background_task']:
                            if msg == 'ERROR':
                                raise Exception("ERROR")
                            if msg == 'CONFIG_NOT_SAVED':
                                raise Exception("CONFIG_NOT_SAVED")
                            time_taken = str((datetime.now() - lapsed_time).seconds)
                            st.write(f"""**Agent:** `{msg}`\n\n**Status:** Completed\n\n**Time:** {time_taken} seconds""")
                            st.divider()
                            lapsed_time = datetime.now()
                            st.session_state['configuration']['stages'].append(msg)
                            total_time += int(time_taken)
                            status_box.update(label="Agent is running ..... (Lapsed Time: " + str(total_time) + " seconds)", state="running", expanded=True)
                        st.session_state['configuration']['status'] = "Reported Generated"
                        status_box.update(label="Generated Report" + " (Total Time taken: " + str(total_time) + " seconds)", state="complete", expanded=True)
                    except Exception as e:
                        if str(e) == 'ERROR':
                            st.toast(f'Please check logs for {st.session_state["configuration"]["uuid"]}')
                            status_box.update(label=f"Please check logs for {st.session_state['configuration']['uuid']}", state="error", expanded=False)
                        if str(e) == 'CONFIG_NOT_SAVED':
                            st.toast(f'Please save the config for {st.session_state["configuration"]["uuid"]}')
                            status_box.update(label=f'Please save the config for {st.session_state["configuration"]["uuid"]}', state="error", expanded=False)
            if st.session_state['configuration']['status'] == "Reported Generated":
                _, col, _ = st.columns(3)
                with col:
                    st.download_button(
                        label="Download HTML Report",
                        data=open(f'./logs/{st.session_state["configuration"]["uuid"]}/index.html', 'rb').read(),
                        file_name=f"{st.session_state['configuration']['uuid']}_report.html",
                        use_container_width=True,
                        mime="text/html",
                    )
            st.session_state['configuration']['background_task'] = None
            st.session_state['configuration']['stages'] = []
            st.session_state['configuration']['status'] = "Initiating Agent ....."
