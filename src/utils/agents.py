from utils.prompt import METADATA_EXTRACTOR_PROMPT

from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model


MODEL_GEMINI = init_chat_model(model="models/gemini-2.5-flash", model_provider="google_genai")


def agent_metadata_extractor():
    """Create a React agent for metadata extraction."""

    # Create the React agent with the metadata extractor tool
    agent = create_react_agent(
        model=MODEL_GEMINI,
        tools=[],
        prompt=METADATA_EXTRACTOR_PROMPT,
    )

    return agent

