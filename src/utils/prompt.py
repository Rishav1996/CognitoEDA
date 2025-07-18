from utils.schema import *
from langchain_core.prompts import PromptTemplate

METADATA_EXTRACTOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are an experienced Data Scientist\n"
        "INSTRUCTIONS : Your objective is to create steps for extracting various types of data information about the data provided. "
        "Only consider metadata information. Assuming you're performing pandas operations\n"
        "EXCLUDE : Any visualization, statistical analysis, loading of data\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

STRUCTURED_FILE_PROMPT = PromptTemplate(
    input_variables=["content", "output_format"],
    template=(
        "ROLE : You are an experienced Software developer, that generates humanly readable documents\n"
        "INSTRUCTIONS : Your objective is to create a structured file format from the dictionary provided.\n"
        "CONTENT : {content}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)
