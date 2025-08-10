import streamlit as st


def show():
    """
    Displays the introductory page of the application.

    This function reads the content of the project's README.md file,
    adjusts an image path to ensure it displays correctly within the
    Streamlit application, and then renders the markdown content on the page.
    A horizontal divider is added at the end for visual separation.
    """
    with open('./README.md', 'r', encoding='utf-8') as f:
        readme = f.read().replace('''---

## 📈 Agentic Workflow

![Application Agentic Workflow](src/static/graph.png)''', '')
        st.markdown(readme, unsafe_allow_html=True)
    st.divider()
