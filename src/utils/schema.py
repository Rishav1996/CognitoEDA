from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class MetadataExtractorOutputFormatSchema(BaseModel):
    output_format: list[str] = Field(
        description="A list of metadata extraction steps to be performed on the data."
    )


class StructuredFileOutputFormatSchema(BaseModel):
    text: str = Field(
        description="The text content of the structured file."
    )


metadata_parser = PydanticOutputParser(
    pydantic_object=MetadataExtractorOutputFormatSchema
)
structured_file_parser = PydanticOutputParser(
    pydantic_object=StructuredFileOutputFormatSchema
)