from typing import TypedDict
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from utils.helper import WorkflowStage

class MetadataExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Metadata Extractor Agent."""
    output_format: list[str] = Field(
        description="A list of the all possible metadata extraction steps to be performed on the data. Example: like extract column information, list of all columns and many more about the data analysis steps. Limit to only : 2"
    )

class StructuredFileOutputFormatSchema(BaseModel):
    """Schema for the output of the Structured File Generator Agent."""
    output_format: str = Field(
        description="The text content of the structured file."
    )

class StatisticsExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Statistics Extractor Agent."""
    output_format: list[str] = Field(
        description="A list of statistical extraction steps to be performed on the data.  Limit to only : 2"
    )

class PythonREPLOutputFormatSchema(BaseModel):
    """Schema for the output of the Python REPL Agent."""
    output_format: str = Field(
        description="The output of the Python Code executed."
    )

class BusinessAnalyticsOutputFormatSchema(BaseModel):
    """Schema for the output of the Business Analytics Agent."""
    output_format: list[str] = Field(
        description="Create an Insight name, Insight Descrition and Insights Generated. Limit to 2"
    )

class HTMLInsightOutputFormatSchema(BaseModel):
    """Schema for the output of the HTML Insight Generator Agent."""
    output_format: str = Field(
        description="The HTML content of the insights generated. Add visuals and charts as needed."
    )


"""Parser for the Metadata Extractor Agent's output."""
metadata_parser = PydanticOutputParser(
    pydantic_object=MetadataExtractorOutputFormatSchema,
)

"""Parser for the Structured File Generator Agent's output."""
structured_file_parser = PydanticOutputParser(
    pydantic_object=StructuredFileOutputFormatSchema
)

"""Parser for the Statistics Extractor Agent's output."""
statistics_parser = PydanticOutputParser(
    pydantic_object=StatisticsExtractorOutputFormatSchema
)

"""Parser for the Python REPL Agent's output."""
python_repl_parser = PydanticOutputParser(
    pydantic_object=PythonREPLOutputFormatSchema
)

"""Parser for the Business Analytics Agent's output."""
business_analytics_parser = PydanticOutputParser(
    pydantic_object=BusinessAnalyticsOutputFormatSchema
)

"""Parser for the HTML Insight Generator Agent's output."""
html_insight_parser = PydanticOutputParser(
    pydantic_object=HTMLInsightOutputFormatSchema
)


FORMAT_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: MetadataExtractorOutputFormatSchema,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: StructuredFileOutputFormatSchema,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: StatisticsExtractorOutputFormatSchema,
    WorkflowStage.PYTHON_CODER_AGENT: PythonREPLOutputFormatSchema,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: BusinessAnalyticsOutputFormatSchema,
    WorkflowStage.WEB_DEVELOPER_AGENT: HTMLInsightOutputFormatSchema
}


PARSER_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: metadata_parser,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: structured_file_parser,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: statistics_parser,
    WorkflowStage.PYTHON_CODER_AGENT: python_repl_parser,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: business_analytics_parser,
    WorkflowStage.WEB_DEVELOPER_AGENT: html_insight_parser
}
