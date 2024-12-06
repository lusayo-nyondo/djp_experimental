import djp
from django.template.library import Library

register = Library()

@register.simple_tag(
    name="djp"
)
def template_includes():
    return str(djp.pm.hook.template_includes())
