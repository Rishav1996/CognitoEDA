from utils.prompt import *
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import json

MODEL_GEMINI = init_chat_model(
    model="models/gemini-2.5-flash",
    model_provider="google_genai"
)


def agent_metadata_extractor(message) -> MetadataExtractorOutputFormatSchema:
    """Create a React agent for metadata extraction."""
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=[],
        prompt=METADATA_EXTRACTOR_PROMPT.format(
            output_format=metadata_parser.get_format_instructions()
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )['messages'][-1].content
    parsed_output = metadata_parser.parse(content)
    return parsed_output


def agent_pandas_dataframe_extractor(df, message):
    """Create a Pandas DataFrame agent for metadata extraction."""
    agent = create_pandas_dataframe_agent(
        MODEL_GEMINI,
        df,
        allow_dangerous_code=True
    )
    content = agent.invoke(message)
    return {"query": message, "answer": content['output']}


def agent_metadata_to_structured_file(question_answer_obj):
    """Convert the question-answer dictionary to a structured file format."""
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=[],
        prompt=STRUCTURED_FILE_PROMPT.format(
            output_format=structured_file_parser.get_format_instructions(),
            content=json.dumps(question_answer_obj)
        )
    )
    content = agent.invoke(
        {"messages": [{"role": "user", "content": "Generate humanly readable structured output"}]}
    )['messages'][-1].content
    parsed_output = structured_file_parser.parse(content)
    return parsed_output
