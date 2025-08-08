import taipy.gui.builder as tgb


with tgb.Page() as intro_page:
    with open('./README.md', mode='r', encoding='utf-8') as fp:
        intro_text = fp.read()
        intro_text = intro_text.replace("""## 📈 Agentic Workflow

![Application Agentic Workflow](src/static/graph.png)

---""", "")
        tgb.text(intro_text, mode="md")