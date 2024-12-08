import djp

@djp.hookimpl
def page_body_includes():
    return """
        <script src="from_plugin.js"></script>
    """.strip()