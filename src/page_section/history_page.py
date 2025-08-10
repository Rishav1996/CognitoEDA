import ast

import pandas as pd
import streamlit as st
from utils.helper import get_logs_info


@st.dialog("View Details", width="large")
def view_dialog(df: pd.DataFrame):
    """
    Creates a dialog box to display details of a selected file from a run.

    This function takes a DataFrame containing information about a single file and
    displays a dialog with options to download or view the file content. The
    content displayed depends on the file type.

    - For `.html` files, it shows an info message and a download button.
    - For `.log` files, it shows an info message and a download button.
    - For `.json` files, it displays the JSON content and provides a download button.
    - For `.csv` files, it displays the first few rows of the data in a
      DataFrame and provides a download button.

    Args:
        df (pd.DataFrame): A DataFrame containing the details of the file to be
                           displayed. It is expected to have a 'path' column
                           with the file path.
    """
    file_path = df['path'].values[0]
    file_name = file_path.split('\\')[-1]

    if file_path.endswith('.html'):
        st.info("Recommend to download webpage.")
        st.download_button(
            label="Download Webpage",
            data=open(file_path, 'rb').read(),
            file_name=file_name,
            use_container_width=False,
            mime="text/html",
        )
    elif file_path.endswith('.log'):
        st.info("Recommend to download log.")
        st.download_button(
            label="Download Log",
            data=open(file_path, 'rb').read(),
            file_name=file_name,
            use_container_width=False,
            mime="text/plain",
        )
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            st.json(ast.literal_eval(f.read().replace("'", '"')))
        st.download_button(
            label="Download JSON",
            data=open(file_path, 'rb').read(),
            file_name=file_name,
            use_container_width=False,
            mime="application/json",
        )
    elif file_path.endswith('.csv'):
        st.info("Recommend to download complete dataset for better view.")
        data = pd.read_csv(file_path).head()
        st.dataframe(data)


def show():
    """
    Displays the history page of the CognitoEDA application.

    This function retrieves and displays the logs of previous EDA runs. It
    fetches all log information, groups the runs by their unique ID, and
    renders each run within a `st.expander`. Each expander shows the run's
    final status (Success/Failed) and provides a set of `st.pills`
    representing the different files/stages of that run.

    When a user selects a pill, this function identifies the corresponding file
    and calls `view_dialog` to display its contents in a modal dialog. It also
    manages the selection state to ensure only one dialog is active at a time.
    """
    st.title("History")
    st.write("To access more insights and individual level info about agents, "
             "run `uv run mlflow server` in your terminal and navigate to the experiment.")

    df = get_logs_info()
    multi_select_value = []
    for uuid in df['uuid'].unique():
        group = df[df['uuid'] == uuid].copy()
        with st.expander(f"Run ID: {uuid}"):
            is_success = list(group['success'].values)[0]
            status = 'Success' if is_success else 'Failed'
            color = 'green' if is_success else 'red'
            icon = '✅' if is_success else '❌'
            st.badge(status, color=color, icon=icon)
            select_value = st.pills("Select File : ", options=group['stage_name'], selection_mode="single", key=uuid)
            if select_value:
                multi_select_value.append([select_value, uuid])
    if len(multi_select_value) > 0:
        filter_df = df[(df['uuid'] == multi_select_value[-1][1]) & (df['stage_name'] == multi_select_value[-1][0])].copy()
    if len(multi_select_value) == 1:
        view_dialog(filter_df)
    elif len(multi_select_value) > 1:
        st.toast('Please unselect previous options')
