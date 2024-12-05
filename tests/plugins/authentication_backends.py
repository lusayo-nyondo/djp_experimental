import djp

@djp.hookimpl
def authentication_backends():
    return [
        'from_plugin.auth_backends.PluginAuthBackend'
    ]
