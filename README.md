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
├── data/
│   ├── temp.csv           # Sample dataset for EDA
│   ├── metadata.txt       # Example output of structured EDA report
│   ├── statistics.txt     # Example output of structured statistics report
│   └── insights.html      # Example output of HTML insights
│
├── src/
│   ├── app.py             # (Entry point for app, if needed)
│   ├── graph.py           # Main workflow script
│   └── utils/
│       ├── __init__.py
│       ├── agents.py      # Agent definitions and orchestration
│       ├── prompt.py      # Prompt templates for LLMs
│       ├── schema.py      # Pydantic schemas and output parsers
│       └── tools.py       # Custom tools for agents
│
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata and dependencies (PEP 621)
└── README.md              # Project documentation
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

## 🚦 Example Usage

1. **Prepare your data:**  
   Place your CSV file in the `data/` directory as `temp.csv`.

2. **Create a virtual environment:**  
   ```bash
   uv venv
   ```

3. **Install dependencies:**  
   ```bash
   uv add -r requirements.txt
   ```

4. **Run the workflow:**  
   ```bash
   uv run src/graph.py
   ```

5. **View the results:**  
   - The generated EDA report will be saved as `data/metadata.txt`.
   - The statistics report will be saved as `data/statistics.txt`.
   - The HTML insights will be saved as `data/insights.html`.

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
- [taipy](https://docs.taipy.io/en/latest/)

---

## ⚠️ Security Notice

The Pandas agent executes code in a Python REPL.  
**Ensure your environment is secure** and do not use untrusted data or prompts.

---

## 🧩 Customization

- **Prompts:**  
  Modify `src/utils/prompt.py` to change how the LLMs are instructed.
- **Schemas:**  
  Update `src/utils/schema.py` to adjust output formats.
- **Agents:**  
  Extend or modify agent logic in `src/utils/agents.py`.
- **Tools:**  
  Add or modify agent tools in `src/utils/tools.py`.

---

## 📄 License

This project is for research and educational purposes.  
Please review dependencies for their respective licenses.
