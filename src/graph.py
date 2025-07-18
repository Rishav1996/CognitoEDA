from dotenv import load_dotenv
import pprint


load_dotenv()

from utils.agents import agent_metadata_extractor

agent = agent_metadata_extractor()


for message in agent.invoke({"messages": [{"role": "user", "content": "Perform EDA"}]})['messages']:
    pprint.pprint(message)
