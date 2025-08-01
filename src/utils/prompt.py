from utils.schema import *
from utils.helper import WorkflowStage
from langchain_core.prompts import PromptTemplate

"""Prompt for the Metadata Extractor Agent."""
METADATA_EXTRACTOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are a proficient Data Analyst\n"
        "TOOLS : {tool_list}\n"
        "GOAL: Write small steps of operations to extract metadata of the dataset\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Structured File Generator Agent."""
STRUCTURED_FILE_PROMPT = PromptTemplate(
    input_variables=["content", "output_format"],
    template=(
        "ROLE : You are a seasoned Software Engineer, adept at crafting easily understandable documentation.\n"
        "GOAL : Your task is to devise a markdown structure representation based on the given dictionary.\n"
        "CONTENT : {content}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Statistics Extractor Agent."""
STATISTICS_EXTRACTOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are a seasoned Data Scientist\n"
        "METADATA : {metadata}\n"
        "GOAL : Your mission is to write quick and small analysis steps for deriving diverse statistical insights from the provided metadata.\n"
        "Investigate novel statistical methodologies and approaches for data analysis, leveraging the aforementioned tools.\n"
        "Focus exclusively on statistical details, specifically employing libraries such as scipy and statsmodels.\n"
        "EXCLUDE : Visual representations, metadata acquisition, and data ingestion.\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the Business Analytics Agent."""
BUSINESS_ANALYTICS_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You function as a seasoned Business Strategist.\n"
        "GOAL : Your aim is to derive strategic business revelations from the supplied metadata and quantitative data.\n"
        "Concentrate exclusively on strategic business implications. Envision yourself executing strategic analysis procedures.\n"
        "EXCLUDE : Visual representations, metadata acquisition, and data ingestion.\n"
        "METADATA : {metadata}\n"
        "STATISTICS : {statistics}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)

"""Prompt for the HTML Insight Generator Agent."""
HTML_INSIGHT_GENERATOR_PROMPT = PromptTemplate(
    input_variables=["output_format"],
    template=(
        "ROLE : You are a seasoned Web Developer\n"
        "GOAL :  Your mission is to develop Interactive Web content and creative charts based on the provided business insights.\n"
        "Focus solely on Interactive Web content creation and creative charts. Envision yourself executing Web operations.\n"
        "INSIGHTS : {insights}\n"
        "METADATA : {metadata}\n"
        "STATISTICS : {statistics}\n"
        "OUTPUT FORMAT : {output_format}"
    ),
)


PROMPT_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: METADATA_EXTRACTOR_PROMPT,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: STRUCTURED_FILE_PROMPT,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: STATISTICS_EXTRACTOR_PROMPT,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: BUSINESS_ANALYTICS_PROMPT,
    WorkflowStage.WEB_DEVELOPER_AGENT: HTML_INSIGHT_GENERATOR_PROMPT
}
