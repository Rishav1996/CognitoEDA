import streamlit as st
from streamlit_option_menu import option_menu

from page_section import agent_page, history_page, intro_page

st.set_page_config(
  page_title="CognitoEDA",
  layout="wide",
  initial_sidebar_state="expanded"
)

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
