import taipy.gui.builder as tgb
from utils.helper import ModelClasses
import pandas as pd
import uuid

"""
TODO :
- add model configs for user to change
- agent sleep time
- agent retry policy
- control panel will show preview of data if not re-upload data
- left section below control panel will show progres of the agent steps and timimngs
- right section below control panel will show the html generated and below html generated convert to pdf or download as html
"""


default_choice_value = ""
default_column_choice = ""
list_of_column_choice = ""
file_path = ""
dataset = pd.DataFrame()
render_file_upload = False
render_choice = False
uuid_name = str(uuid.uuid4())
control_panel_bool = True


def on_init(state):
    state.render_file_upload = True
    state.render_choice = False


def check_file_upload(state):
    if state.file_path != "":
        global dataset
        dataset = pd.read_csv(state.file_path)
        state.list_of_column_choice = list(dataset.columns)
        state.render_file_upload = False
        state.render_choice = True


def on_trigger(state):
    state.control_panel_bool = False


with tgb.Page() as agent_page:
    tgb.text("# **Agentic Workflow**", mode="md")
    with tgb.part(class_name="card", render="{render_file_upload}"):
        tgb.text("Control Panel", mode="md")
        with tgb.layout(columns="20% 60% 20%"):
            tgb.part()
            tgb.file_selector("{file_path}", label="Upload your dataset",
                                on_action=check_file_upload, extensions=".csv", multiple=False)
            tgb.part()
    with tgb.part(class_name="card", render="{render_choice}"):
        tgb.text("Control Panel", mode="md")
        with tgb.layout(columns="20% 30% 30% 20%"):
            tgb.part()
            tgb.selector("{default_choice_value}",
                        lov=" ;".join([model.value for model in ModelClasses]),
                        dropdown=True, label="Choice of use case")
            tgb.selector("{default_column_choice}", lov="{list_of_column_choice}",
                        dropdown=True, label="Choose target column")
            tgb.part()
        with tgb.layout(columns="20% 60% 20%"):
            tgb.part()
            tgb.button("Trigger Agent", on_action=on_trigger)
            tgb.part()
    with tgb.part():
        with tgb.layout(columns="50% 50%"):
            tgb.part(class_name="card")
            tgb.part(class_name="card")
