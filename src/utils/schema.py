from pydantic import BaseModel, Field


class MetadataExtractorOutputFormatSchema(BaseModel):
    output_format: list[str] = Field(
        description="A list of metadata extraction steps to be performed on the data."
    )