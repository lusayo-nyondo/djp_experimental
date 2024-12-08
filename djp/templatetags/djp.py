import djp
from django.template.library import Library
from django.utils.safestring import (
    mark_safe
)


register = Library()


@register.simple_tag(
    name="djp_page_head_includes",
)
def page_head_includes():
    template_includes = str(djp.pm.hook.page_head_includes())
    return mark_safe(template_includes)


@register.simple_tag(
    name="djp_page_body_includes"
)
def page_body_includes():
    template_includes = str(djp.pm.hook.page_body_includes())
    return mark_safe(template_includes)

