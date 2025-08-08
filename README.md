# 🚀 CognitoEDA

**CognitoEDA** is an agentic workflow for automated Exploratory Data Analysis (EDA) using Large Language Models (LLMs) and Pandas. The project leverages LangChain, LangGraph, and Google Gemini models to extract metadata, generate EDA queries, and produce human-readable structured reports from tabular data.

---

## ✨ Features

- **Automated Metadata Extraction:**  
  Uses LLM agents to analyze a DataFrame and suggest relevant EDA steps.
- **Agentic Query Execution:**  
  Dynamically executes EDA queries on your data using a secure, sandboxed Python environment.
- **Structured Reporting:**  
  Converts EDA results into a human-friendly, structured document.
- **Extensible Workflow:**  
  Modular design for easy extension with new agents, prompts, or data sources.

---

## 📁 Project Structure

```
CognitoEDA/
│
├── src/
│   ├── app.py             # Main Streamlit application
│   ├── graph.py           # Core agentic workflow logic
│   ├── page_section/      # Streamlit pages for the UI
│   │   ├── agent_page.py
│   │   ├── history_page.py
│   │   └── intro_page.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── agents.py      # Agent definitions
│   │   ├── helper.py      # Helper functions
│   │   ├── prompt.py      # Prompt templates
│   │   ├── schema.py      # Pydantic schemas
│   │   └── tools.py       # Custom tools for agents
│   └── utils/             # Utility scripts
│
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```

---

## ⚙️ How It Works

1. **Metadata Extraction:**  
   The workflow starts by prompting an LLM agent to suggest EDA steps based on the dataset and use case (e.g., classification).
2. **Query Execution:**  
   Each suggested EDA step is executed on the DataFrame using a Pandas agent, and the results are collected.
3. **Structured Output:**  
   The question-answer pairs are converted into a readable report using another LLM agent, following a structured template.
4. **Statistics Extraction:**  
   Additional statistical steps are generated and executed, with results saved in a structured format.
5. **Business Insights & HTML Generation:**  
   Business insights are generated from metadata/statistics, and then converted into interactive HTML reports.

---

## 📈 Agentic Workflow

![Application Agentic Workflow](src/static/graph.png)

---

## 🚦 Example Usage

1. **Create a virtual environment:**  
   ```bash
   uv venv
   ```

2. **Install dependencies:**  
   ```bash
   uv add -r requirements.txt
   ```

3. **Run the application:**  
   ```bash
   uv run streamlit run ./src/app.py
   ```

4. **Access the application:**  
   Open your web browser and navigate to the URL provided by Streamlit (usually `http://127.0.0.1:8501`).

---

## 📝 Requirements

- Python 3.11+
- All dependencies are listed in [`requirements.txt`](requirements.txt) and [`pyproject.toml`](pyproject.toml).

---

## 🛠️ Key Technologies

- [LangChain](https://python.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini (via LangChain)](https://python.langchain.com/docs/integrations/chat/google_genai)
- [Pandas](https://pandas.pydata.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [MLflow](https://mlflow.org/)
- [pytest](https://docs.pytest.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [arxiv](https://pypi.org/project/arxiv/)
- [duckduckgo-search](https://pypi.org/project/duckduckgo-search/)
- [streamlit](https://docs.streamlit.io/)

---

## ⚠️ Security Notice

The Pandas agent executes code in a Python REPL.  
**Ensure your environment is secure** and do not use untrusted data or prompts.

---

## 🧩 Customization

- **Prompts:**  
  Modify `src/tools/prompt.py` to change how the LLMs are instructed.
- **Schemas:**  
  Update `src/tools/schema.py` to adjust output formats.
- **Agents:**  
  Extend or modify agent logic in `src/tools/agents.py`.
- **Tools:**  
  Add or modify agent tools in `src/tools/tools.py`.

---

## 📄 License

This project is for research and educational purposes. Please review dependencies for their respective licenses.