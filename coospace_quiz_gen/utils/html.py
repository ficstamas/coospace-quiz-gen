def format_html_for_json_data(text):
    t = text
    t = t.replace("<br>", "<br/>")
    t = t.replace("<", "&lt;").replace(">", "&gt;")
    return t