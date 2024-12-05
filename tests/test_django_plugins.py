from django.conf import settings
from django.test.client import Client
import httpx
import pytest


def test_middleware_order():
    assert settings.MIDDLEWARE == [
        "tests.test_project.middleware.MiddlewareBefore",
        "tests.test_project.middleware.Middleware",
        "tests.test_project.middleware.Middleware4",
        "tests.test_project.middleware.Middleware2",
        "tests.test_project.middleware.Middleware5",
        "tests.test_project.middleware.Middleware3",
        "tests.test_project.middleware.MiddlewareAfter",
    ]


def test_middleware():
    response = Client().get("/")
    assert response["X-DJP-Middleware-After"] == "MiddlewareAfter"
    assert response["X-DJP-Middleware"] == "Middleware"
    assert response["X-DJP-Middleware-Before"] == "MiddlewareBefore"
    request = response._request
    assert hasattr(request, "_notes")
    assert request._notes == [
        "MiddlewareAfter",
        "Middleware3",
        "Middleware5",
        "Middleware2",
        "Middleware4",
        "Middleware",
        "MiddlewareBefore",
    ]


def test_urlpatterns():
    response = Client().get("/from-plugin/")
    assert response.content == b"Hello from a plugin"


def test_settings():
    assert settings.FROM_PLUGIN == "x"


def test_installed_apps():
    assert "tests.test_project.app1" in settings.INSTALLED_APPS


def test_databases():
    assert "from_plugin" in settings.DATABASES.keys()


def test_context_processors():
    assert 'from_plugin.context_processors.my_context_processor' \
        in settings.TEMPLATES[0]["OPTIONS"]['context_processors']


def test_loaders():
    assert 'from_plugin.loaders.my_plugin_loader' \
        in settings.TEMPLATES[0]["OPTIONS"]['loaders']

     
def test_builtins():
    assert 'from_plugin.templatetags.my_plugin_tags' \
        in settings.TEMPLATES[0]["OPTIONS"]['builtins']
        
def test_staticfiles_dirs():
    assert 'from_plugin_staticfiles_dir' \
        in settings.STATICFILES_DIRS
        
def test_staticfiles_finders():
    assert 'from_plugin.finders.PluginFinder' \
        in settings.STATICFILES_FINDERS
        
def test_authentication_backends():
    assert 'from_plugin.auth_backends.PluginAuthBackend' \
        in settings.AUTHENTICATION_BACKENDS
        
def test_auth_password_validators():
    print(settings.AUTH_PASSWORD_VALIDATORS)
    assert {
        'NAME': 'from_plugin.auth_password_validators.PluginAuthPasswordValidator'
    } in settings.AUTH_PASSWORD_VALIDATORS


@pytest.mark.asyncio
async def test_asgi_wrapper():
    from django.core.asgi import get_asgi_application
    from djp import asgi_wrapper

    application = get_asgi_application()
    wrapped_application = asgi_wrapper(application)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped_application),
        base_url="http://testserver",
    ) as client:
        response = await client.get("http://testserver/hello")
        assert response.status_code == 200
        assert response.text == "Hello world"
