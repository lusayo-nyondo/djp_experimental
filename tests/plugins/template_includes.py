from django.urls import path
from django.http import HttpResponse
import djp


@djp.hookimpl
def template_includes():
    return """
        {% autoescape off %}
        <script src="from_plugin.js"></script>
        {% endautoescape %}
    """.strip()
