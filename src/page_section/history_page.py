import streamlit as st
import pandas as pd
import ast
from utils.helper import get_logs_info


@st.dialog("View Details", width="large")
def view_dialog(df):
    file_path = df['path'].values[0]
    if file_path.endswith('.html'):
        st.info("Recommend to download webpage.")
        st.download_button(
            label="Download Webpage",
            data=open(file_path, 'rb').read(),
            file_name=file_path.split('\\')[-1],
            use_container_width=False,
            mime="text/plain",
        )
    if file_path.endswith('.log'):
        st.info("Recommend to download log.")
        st.download_button(
            label="Download Log",
            data=open(file_path, 'rb').read(),
            file_name=file_path.split('\\')[-1],
            use_container_width=False,
            mime="text/plain",
        )
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            st.json(ast.literal_eval(f.read().replace("'", '"')))
        st.download_button(
            label="Download JSON",
            data=open(file_path, 'rb').read(),
            file_name=file_path.split('\\')[-1],
            use_container_width=False,
            mime="text/plain",
        )
    if file_path.endswith('.csv'):
        st.info("Recommend to download complete dataset for better view.")
        data = pd.read_csv(file_path).head()
        st.dataframe(data)


def show():
    st.title("History")
    df = get_logs_info()
    grouped_by_uuid = df.groupby('uuid')
    multi_select_value = []
    for uuid, group in grouped_by_uuid:
        with st.expander(f"Run ID: {uuid}"):
            status = 'Success' if list(group['success'].values)[0] else 'Failed'
            color = 'green' if list(group['success'].values)[0] else 'red'
            icon = '✅' if list(group['success'].values)[0] else '❌'
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
