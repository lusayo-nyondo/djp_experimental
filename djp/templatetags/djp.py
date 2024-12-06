import djp
from django.template.library import Library

register = Library()

@register.simple_tag(
    name="djp"
)
def template_includes():
    template_includes = str(djp.pm.hook.template_includes())
    return template_includes
