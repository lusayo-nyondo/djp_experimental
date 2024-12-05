import djp

@djp.hookimpl
def staticfiles_dirs():
    return [
        'from_plugin_staticfiles_dir'
    ]
