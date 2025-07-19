from utils.schema import *
from langchain_core.prompts import PromptTemplate

"""Prompt for the Metadata Extractor Agent."""
METADATA_EXTRACTOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Data Scientist\n"
        "INSTRUCTIONS : Your objective is to create steps for extracting various types of data information about the data provided. "
        "TOOLS : You have access to {tool_list} these tools to perform the task.\n"
        "Only consider metadata information. Assuming you're performing pandas operations\n"
        "EXCLUDE : Any visualization, statistical analysis, loading of data\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Structured File Generator Agent."""
STRUCTURED_FILE_PROMPT = PromptTemplate(
    input_variables=["content", "output_format"],
    template=(
        "ROLE : You are an experienced Software developer, that generates humanly readable documents\n"
        "INSTRUCTIONS : Your objective is to create a structured file format from the dictionary provided.\n"
        "CONTENT : {content}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Statistics Extractor Agent."""
STATISTICS_EXTRACTOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Data Scientist\n"
        "METADATA : {metadata}\n"
        "TOOLS : You have access to {tool_list} these tools to perform the task.\n"
        "INSTRUCTIONS : Your objective is to create steps for extracting various types of statistical information refer the metadata provided.\n"
        "Explore new statistical methods and techniques to analyze the data. Using the above tools mentioned\n"
        "Only consider statistical information. Consider libraries like scipy, and statsmodels only\n"
        "EXCLUDE : Any visualization, metadata extraction, loading of data\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Python REPL Agent."""
PYTHON_REPL_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Python Developer\n"
        "TOOLS : You have access to {tool_list} these tools to perform the task.\n"
        "INSTRUCTIONS : Your objective is to create a python function for the task given and execute python code using the tools\n"
        "Only consider Python code execution. Assuming you're performing Python operations\n"
        "TASK : {task}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Business Analytics Agent."""
BUSINESS_ANALYTICS_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Business Analyst\n"
        "TOOLS : You have access to {tool_list} these tools to perform the task.\n"
        "INSTRUCTIONS : Your objective is to create business insights from the metadata & statistical information provided.\n"
        "Only consider business insights. Assuming you're performing business analysis operations.\n"
        "Also use Python REPL tool to generate graphs from the DataFrame 'df' and statistical analysis and return bytes output using `io` library\n"
        "METADATA : {metadata}\n"
        "STATISTICS : {statistics}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the HTML Insight Generator Agent."""
HTML_INSIGHT_GENERATOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Web Developer\n"
        "TOOLS : You have access to {tool_list} these tools to perform the task.\n"
        "INSTRUCTIONS : Your objective is to create Web content for the business insights generated.\n"
        "Only consider Web content generation. Assuming you're performing Web operations. Add images and beautiful charts\n"
        "Added metadata and statistics for your reference to create interactive images and charts.\n"
        "Also added dataframe to generate images and charts\n"
        "INSIGHTS : {insights}\n"
        "METADATA : {metadata}\n"
        "DATAFRAME : {dataframe}\n"
        "STATISTICS : {statistics}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)