import djp

@djp.hookimpl
def auth_password_validators():
    return [{
        'NAME': 'from_plugin.auth_password_validators.PluginAuthPasswordValidator'  
    },]
