import djp

@djp.hookimpl
def databases():
    databases = {
        'from_plugin': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    return databases
