from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from utils.helper import WorkflowStage

class MetadataExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Metadata Extractor Agent."""
    output_format: list[str] = Field(
        description="A list of metadata extraction steps to be performed on the data."
    )

class StructuredFileOutputFormatSchema(BaseModel):
    """Schema for the output of the Structured File Generator Agent."""
    output_format: str = Field(
        description="The text content of the structured file."
    )

class StatisticsExtractorOutputFormatSchema(BaseModel):
    """Schema for the output of the Statistics Extractor Agent."""
    output_format: list[str] = Field(
        description="A list only 2 statistical extraction steps to be performed on the data."
    )

class PythonREPLOutputFormatSchema(BaseModel):
    """Schema for the output of the Python REPL Agent."""
    output_format: str = Field(
        description="The output of the Python Code executed."
    )

class GraphFormatSchema(BaseModel):
    """Schema for the output of the Graph Agent."""
    graph_name: str = Field(
        description="The name of the graph to be generated."
    )
    graph_description: str = Field(
        description="A detailed description of the graph what needs to be generated and how it should be visualized."
    )
    graph_type: str = Field(
        description="The type of graph to be generated (e.g., bar chart, line chart, scatter plot and many more)."
    )

class BusinessAnalyticsInsightFormatSchema(BaseModel):
    """Schema for a single business insight."""
    insight_name: str = Field(
        description="The name of the business insight."
    )
    insight_description: str = Field(
        description="A detailed description of the business insight."
    )
    insights_generated: list[str] = Field(
        description="A list of insights generated from the metadata and statistical information."
    )
    insights_graph: list[GraphFormatSchema] = Field(
        description="A list of graphs to be generated for the insight."
    )

class BusinessAnalyticsOutputFormatSchema(BaseModel):
    """Schema for the output of the Business Analytics Agent."""
    output_format: list[BusinessAnalyticsInsightFormatSchema] = Field(
        description="A list of business insights to be generated."
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


PARSER_MAPPER = {
    WorkflowStage.METADATA_EXTRACTOR_AGENT: metadata_parser,
    WorkflowStage.STRUCTURE_CREATOR_AGENT: structured_file_parser,
    WorkflowStage.STATISTICS_GENERATOR_AGENT: statistics_parser,
    WorkflowStage.PYTHON_CODER_AGENT: python_repl_parser,
    WorkflowStage.BUSINESS_INSIGHTS_AGENT: business_analytics_parser,
    WorkflowStage.WEB_DEVELOPER_AGENT: html_insight_parser
}
