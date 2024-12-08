import djp


@djp.hookimpl
def page_head_includes():
    return """
        <link href="from_plugin.css" type="text/css" rel="stylesheet">
    """.strip()
