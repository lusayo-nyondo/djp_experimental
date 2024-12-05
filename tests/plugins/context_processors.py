import djp

@djp.hookimpl
def context_processors():
    return [
        'from_plugin.context_processors.my_context_processor',
    ]