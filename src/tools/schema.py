from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from tools.helper import WorkflowStage

class MetadataExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Metadata Extractor Agent."""
    output_format: List[str] = Field(
        description="Provide a comprehensive list of metadata items, like Dataset Dimensions, Column Details and many more",
        max_items=10
    )

class StructuredFileOutputFormatSchema(BaseModel):
    """Schema for the output of the Structured File Generator Agent."""
    output_format: str = Field(
        description="The text content of the structured file."
    )

class StatisticsExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Statistics Extractor Agent."""
    output_format: List[str] = Field(
        description="A list of statistical extraction steps to be performed on the data.",
        max_items=20
    )

class PythonREPLOutputFormatSchema(BaseModel):
    """Schema for the output of the Python REPL Agent."""
    output_format: str = Field(
        description="Output from the Python code's run"
    )

class BusinessAnalyticsOutputFormatSchema(BaseModel):
    """Schema for the output of the Business Analytics Agent."""
    output_format: List[str] = Field(
        description="Create an Insight name, Insight Descrition and Insights Generated.",
        max_items=20
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
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: BusinessAnalyticsOutputFormatSchema,
    WorkflowStage.WEB_DEVELOPER_AGENT: HTMLInsightOutputFormatSchema
}


PARSER_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: metadata_parser,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: structured_file_parser,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: statistics_parser,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: business_analytics_parser,
    WorkflowStage.WEB_DEVELOPER_AGENT: html_insight_parser
}
