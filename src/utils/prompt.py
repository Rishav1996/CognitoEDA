from utils.schema import MetadataExtractorOutputFormatSchema

from langchain_core.output_parsers import PydanticOutputParser


metadata_parser = PydanticOutputParser(pydantic_object=MetadataExtractorOutputFormatSchema)

METADATA_EXTRACTOR_PROMPT = f""""ROLE : You are an experienced Data Scientist
INSTRUCTIONS : Your objective is to create steps for extracting various types of data information about the data provided. Only consider metadata information. Assuming your performing pandas operations
EXCLUDE : Any visualization, statistical analysis, loading of data
OUTPUT FORMAT : {metadata_parser.get_format_instructions()}"""
