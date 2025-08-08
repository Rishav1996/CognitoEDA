from taipy.gui import Gui, navigate
import taipy.gui.builder as tgb

from pages.agent_page import *
from pages.introduction_page import *
from pages.history_page import *


def menu_option_selected(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)

with tgb.Page() as root_page:
    tgb.menu(label="Menu",
            lov=[('intro', 'Introduction'),('agent', 'Agent'), ('history', 'History')],
            on_action=menu_option_selected)

pages ={'/': root_page, 'intro': intro_page, 'agent': agent_page, 'history': history_page}

if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(title="CognitoEDA", use_reloader=True, dark_mode=False, allow_unsafe_werkzeug=True, port=5050)
