import djp

@djp.hookimpl
def builtins():
    return [
        'from_plugin.templatetags.my_plugin_tags'
    ]