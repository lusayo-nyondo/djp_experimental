from django.urls import path
from django.http import HttpResponse
import djp


@djp.hookimpl
def template_includes():
    return """
        <script src="from_plugin.js"></script>
    """.strip()
