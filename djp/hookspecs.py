from pluggy import HookimplMarker
from pluggy import HookspecMarker

hookspec = HookspecMarker("djp")
hookimpl = HookimplMarker("djp")


@hookspec
def installed_apps():
    """Return a list of Django app strings to be added to INSTALLED_APPS"""


@hookspec
def middleware():
    """
    Return a list of Django middleware class strings to be added to MIDDLEWARE.
    Optionally wrap with djp.Before() or djp.After() to specify ordering,
    or wrap with djp.Position(name, before=other_name) to insert before another
    or djp.Position(name, after=other_name) to insert after another.
    """


@hookspec
def urlpatterns():
    """Return a list of url patterns to be added to urlpatterns"""


@hookspec
def settings(current_settings):
    """Modify current_settings in place to finish configuring settings.py"""


@hookspec
def asgi_wrapper():
    """Returns an ASGI middleware callable to wrap our ASGI application with"""
  

@hookspec
def databases():
    """
    Returns a list of Database specs that can be added to the project's
    DATABASES setting.
    """
 
  
@hookspec
def context_processors():
    """
    Returns a list of Python package strings to be added as context_processors
    for Django's templating engine.
    """


@hookspec
def builtins():
    """
    Returns a list of Python template tag packages to be added as builtins
    for Django's templating engine.
    """

@hookspec
def staticfiles_dirs():
    """
    Returns a list of class name strings that are added to the project's default
    STATICFILES_DIRS setting for Django's templating engine if it exists.
    """

    
@hookspec
def staticfiles_finders():
    """
    Returns a list of class name strings that are added to the project's default
    STATICFILES_FINDERS setting for Django's templating engine if it exists.
    """


@hookspec
def auth_password_validators():
    """
    Returns a list of Auth password validators that can be added to
    the project's AUTH_PASSWORD_VALIDATORS setting.
    """


@hookspec
def authentication_backends():
    """
    Returns a list of Authentication backends that can be added to
    the project's Authentication backends.
    """


@hookspec
def admin_sidebar_items():
    """
    Returns a list of items to be placed on the admin sidebar.
    This uses django unfold.
    """


@hookspec
def page_head_includes():
    """
    Returns a list of arbitrary strings that are included inside project templates.
    Right now, without validation, introduces the possibility of a plugin breaking the entire
    templating engine, so validation must be added later to make sure that what's being included
    are only valid HTML tags that make sense to be inside the head.
    """


@hookspec
def page_body_includes():
    """
    Returns a list of arbitrary strings that are included inside project template body right
    before the closing body tag. Right now, without validation, introduces the possibility of
    a plugin breaking the entire templating engine, so validation must be added later.
    I also need to add ordering.
    """