import logging
from dotenv import load_dotenv
import time
import pandas as pd
from utils.agents import *


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

load_dotenv()

df = pd.read_csv("./data/temp.csv")  # Load your DataFrame here

logging.info("Starting metadata extraction...")

target_column = "AHD"
type_of_use_case = "classification"

prompt = (
    f"Perform all EDA steps keeping target column as '{target_column}' "
    f"and this is a {type_of_use_case} use case"
)

json_message = agent_metadata_extractor(prompt)
logging.info("Metadata extraction complete.")

time.sleep(10)

question_answer = []

for query in json_message.output_format:
    logging.info(f"Processing query: {query}")
    output = agent_pandas_dataframe_extractor(df, query)
    logging.info("Query processed")
    time.sleep(10)
    question_answer.append(output)

logging.info("Converting question-answer pairs to structured file format...")
structured_file = agent_metadata_to_structured_file(question_answer)
logging.info("Structured file created.")

print(structured_file.text)


# Save the structured file to a text file
with open("./data/metadata.txt", "w") as file:
    file.write(structured_file.text)
