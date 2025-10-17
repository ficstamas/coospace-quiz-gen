def format_html_for_json_data(text):
    t = text
    t = t.replace("<br>", "<br/>")
    # TODO there is a difference between the format of HTML tags and random "<" symbols, such as "p <= 0.1"
    t = t.replace("<", "&lt;").replace(">", "&gt;")
    return t