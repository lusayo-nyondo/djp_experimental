import djp

@djp.hookimpl
def staticfiles_finders():
    return [
        'from_plugin.finders.PluginFinder'
    ]