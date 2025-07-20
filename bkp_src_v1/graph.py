import logging
import os
from dotenv import load_dotenv
import time
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

load_dotenv()

from utils.agents import *

# Sleep duration (in seconds) between agent calls
AGENT_SLEEP_SECONDS = 20

# Load the main DataFrame from CSV
df = pd.read_csv("./data/temp.csv")  # Load your DataFrame here

logging.info("Starting metadata extraction...")

# Define the target column and use case type for EDA
target_column = "AHD"
type_of_use_case = "classification"
n_steps = 5

# Create the initial prompt for metadata extraction
if target_column != None:
    prompt = (
        f"Create {n_steps} steps for the EDA consider target column as '{target_column}' "
        f"and this is a {type_of_use_case} use case"
    )
else:
    prompt = (
        f"Create {n_steps} steps for the EDA and this is a {type_of_use_case} use case"
    )

# Extract metadata using the agent
json_message = agent_metadata_extractor(prompt)
logging.info("Metadata extraction complete.")

time.sleep(AGENT_SLEEP_SECONDS)

# List to store question-answer pairs for EDA
question_answer = []

# Process each EDA query and collect results
for query in json_message.output_format:
    logging.info("Processing query")
    output = agent_pandas_dataframe_extractor(df, query)
    logging.info("Query processed")
    time.sleep(AGENT_SLEEP_SECONDS)
    question_answer.append(output)

logging.info("Converting question-answer pairs to structured file format...")
structured_file = agent_metadata_to_structured_file(question_answer)
logging.info("Structured file created.")

# Save the structured file to a text file
with open("./data/metadata.txt", "w") as file:
    file.write(structured_file.text)

# Extract statistics using the agent
statistics_output = agent_statistics_extractor()
logging.info("Statistics extraction complete.")

time.sleep(AGENT_SLEEP_SECONDS)

# List to store question-answer pairs for statistics
question_answer = []

# Process each statistics query and collect results
for query in statistics_output.output_format:
    logging.info("Processing query")
    output = agent_python_repl(df, query)
    logging.info("Query processed")
    time.sleep(AGENT_SLEEP_SECONDS)
    question_answer.append(output)

logging.info("Converting question-answer pairs to structured file format for statistics...")
structured_file = agent_metadata_to_structured_file(question_answer)
logging.info("Structured file for statistics created.")

# Save the structured file for statistics to a text file
with open("./data/statistics.txt", "w") as file:
    file.write(structured_file.text)

logging.info("Starting business insights generation...")
business_insights = agent_business_insight_generator(df)
logging.info("Business insights generation complete.")

logging.info("Starting HTML insights generation...")
html_insights = agent_html_insight_generator(df, business_insights)
logging.info("HTML insights generation complete.")

# Save the HTML insights to a file
with open("./data/insights.html", "w") as file:
    file.write(html_insights.output_format)
