from django.template.library import Library

register = Library()

@register.simple_tag(
    name="plugin_template_tag"
)
def plugin_template_tag():
    return "Plugin template tag."