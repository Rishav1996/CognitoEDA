import streamlit as st


def show():
    with open('./README.md', 'r', encoding='utf-8') as f:
        readme = f.read().replace('src/static/graph.png', './src/static/graph.png')
        st.markdown(readme, unsafe_allow_html=True)
    st.divider()
