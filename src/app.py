"""Project Starting Point"""

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from graph import set_mlflow
from page_section import agent_page, history_page, intro_page

st.set_page_config(
  page_title="CognitoEDA",
  layout="wide",
  initial_sidebar_state="expanded"
)

if 'configuration' not in st.session_state:
    st.session_state['configuration'] = {
            'agent_sleep_seconds': 30,
            'temperature': 1.0,
            'problem_type': None,
            'target_column': None,
            'data_table': pd.DataFrame(),
            'uuid': None,
            'stages': [],
            'status': "Initiating Agent .....",
            'background_task': None
        }

if 'configuration' in st.session_state:
    st.session_state['configuration']['data_table'] = pd.DataFrame()

set_mlflow()

with st.sidebar:
    selected = option_menu(
        None,
        ["Introduction", "Agent", "History"],
        icons=["house-door-fill", "robot", "clock-history"],
        default_index=0,
    )

if selected == "Introduction":
    intro_page.show()
elif selected == "Agent":
    agent_page.show()
elif selected == "History":
    history_page.show()
