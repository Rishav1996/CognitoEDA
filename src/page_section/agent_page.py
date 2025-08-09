# import streamlit as st
# import pandas as pd
# import time
# from threading import Thread
# from streamlit.runtime.scriptrunner import add_script_run_ctx
# from io import BytesIO

# # --- Session State Initialization (kept at top level) ---
# # This is crucial for managing the application's state across reruns.
# if 'agents' not in st.session_state:
#     st.session_state.agents = {}  # Stores agent data: status, progress, time
# if 'uploaded_file' not in st.session_state:
#     st.session_state.uploaded_file = None
# if 'df' not in st.session_state:
#     st.session_state.df = pd.DataFrame()

# # --- Background Agent Function (kept at top level) ---
# def run_agent_in_background(agent_id, config):
#     """
#     Simulates a long-running agent process.
#     Updates st.session_state to show progress in the UI.
#     """
#     st.session_state.agents[agent_id]['status'] = 'Running'
#     st.session_state.agents[agent_id]['progress'] = 0
#     start_time = time.time()
    
#     st.rerun()

#     for i in range(1, 11):
#         time.sleep(config['agent_sleep_seconds'] / 10)
#         st.session_state.agents[agent_id]['progress'] = i * 10
#         st.session_state.agents[agent_id]['time_elapsed'] = time.time() - start_time
#         st.rerun()

#     st.session_state.agents[agent_id]['status'] = 'Completed'
#     st.session_state.agents[agent_id]['progress'] = 100
#     st.session_state.agents[agent_id]['time_elapsed'] = time.time() - start_time
#     st.rerun()

# # --- Main UI Function ---
# def show():
#     """
#     Encapsulates all the Streamlit UI components and logic.
#     """
#     st.set_page_config(layout="wide")
#     st.title("Agentic Workflow")

#     # --- Collapsible Control Panel ---
#     with st.expander("Agent & Data Configuration", expanded=False):
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.subheader("MLflow Server")
#             mlflow_port = st.text_input("Port Number", value="5000")
            
#             st.subheader("Agent Configuration")
#             agent_sleep_seconds = st.number_input("Agent Sleep Seconds", min_value=1, value=5)
        
#         with col2:
#             st.subheader("Retry Policy")
#             max_attempts = st.number_input("Maximum Attempts", min_value=1, value=3)
#             min_interval = st.number_input("Minimum Interval (sec)", min_value=1, value=10)
#             max_interval = st.number_input("Maximum Interval (sec)", min_value=1, value=60)
            
#         with col3:
#             st.subheader("Dataset & Modeling")
#             uploaded_file = st.file_uploader("Upload CSV Dataset", type=['csv'])
#             if uploaded_file is not None:
#                 st.session_state.uploaded_file = uploaded_file
#                 st.session_state.df = pd.read_csv(uploaded_file)
#                 problem_type = st.selectbox("Problem Type", ["Classification", "Regression"])
                
#                 columns = st.session_state.df.columns.tolist()
#                 target_column = st.selectbox("Select Target Column", options=columns)

#         if st.button("Save Config", type="primary"):
#             if st.session_state.uploaded_file:
#                 agent_id = f"Agent_{len(st.session_state.agents) + 1}"
                
#                 config = {
#                     'mlflow_port': mlflow_port,
#                     'agent_sleep_seconds': agent_sleep_seconds,
#                     'retry_policy': {'max_attempts': max_attempts, 'min_interval': min_interval, 'max_interval': max_interval},
#                     'problem_type': problem_type,
#                     'target_column': target_column,
#                     'data_source': uploaded_file.name
#                 }
                
#                 st.session_state.agents[agent_id] = {'status': 'Starting', 'progress': 0, 'time_elapsed': 0, 'config': config}
                
#                 thread = Thread(target=run_agent_in_background, args=(agent_id, config))
#                 add_script_run_ctx(thread)
#                 thread.start()
#                 st.rerun()
#             else:
#                 st.error("Please upload a CSV file first.")

#     st.divider()

#     # --- Main Dashboard Layout ---
#     col_left, col_right = st.columns(2)

#     with col_left:
#         st.subheader("Data Viewer")
#         if not st.session_state.df.empty:
#             st.dataframe(st.session_state.df)
#         else:
#             st.info("Upload a dataset to view its contents.")

#     with col_right:
#         st.subheader("Agent Status Dashboard")
#         if not st.session_state.agents:
#             st.info("No agents are currently running.")
        
#         for agent_id, agent_info in st.session_state.agents.items():
#             with st.status(f"**{agent_id}** - Status: {agent_info['status']}", expanded=True):
#                 st.write(f"Time Elapsed: {agent_info['time_elapsed']:.2f} seconds")
#                 st.progress(agent_info['progress'], text=f"{agent_info['progress']}%")
                
#                 if st.button("View Log Summary", key=f"log_{agent_id}"):
#                     st.write("---")
#                     st.subsubheader("GenAI Log Summary")
#                     st.write("A GenAI model would summarize the agent's run logs here, highlighting key steps and results.")
                
#                 if agent_info['status'] == 'Completed':
#                     report_content = "This is a placeholder HTML report for the agent's run."
#                     st.download_button(
#                         label="Download HTML Report",
#                         data=report_content.encode('utf-8'),
#                         file_name=f"{agent_id}_report.html",
#                         mime="text/html",
#                         key=f"download_{agent_id}"
#                     )

import streamlit as st
import uuid


def show():
    st.set_page_config(layout="wide")
    st.title("Agentic Workflow")
    uuid_num = str(uuid.uuid4())
    with st.expander("Agent & Data Configuration", expanded=False):
        agent_config_col, data_config_col = st.columns(2)
        with agent_config_col:
            st.text("Agent Configuration")
        with data_config_col:
            st.text("Dataset Configuration")
    data_view_col, agent_status_col = st.columns(2)
    with data_view_col:
        with st.container(border=True):
            st.text("Data Viewer")
    with agent_status_col:
        with st.container(border=True):
            st.text("Agent Status Dashboard")
