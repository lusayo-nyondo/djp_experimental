from .hookspecs import hookimpl
from . import hookspecs
from .lib import (
    setting_exists
)
import itertools
import os
import pathlib
from pluggy import PluginManager
import sys
from typing import List
import types

pm = PluginManager("djp")
pm.add_hookspecs(hookspecs)
pm.load_setuptools_entrypoints("djp")


def _module_from_path(path, name):
    # Adapted from http://sayspy.blogspot.com/2011/07/how-to-import-module-from-just-file.html
    mod = types.ModuleType(name)
    mod.__file__ = path
    with open(path, "r") as file:
        code = compile(file.read(), path, "exec", dont_inherit=True)
    exec(code, mod.__dict__)
    return mod


plugins_dir = os.environ.get("DJP_PLUGINS_DIR")
if plugins_dir:
    for filepath in pathlib.Path(plugins_dir).glob("*.py"):
        mod = _module_from_path(str(filepath), name=filepath.stem)
        try:
            pm.register(mod)
        except ValueError as ex:
            print(ex, file=sys.stderr)
            # Plugin already registered
            pass


class Before:
    def __init__(self, item: str):
        self.item = item


class After:
    def __init__(self, item: str):
        self.item = item


class Position:
    def __init__(self, item: str, before=None, after=None):
        assert not (before and after), "Cannot specify both before and after"
        self.item = item
        self.before = before
        self.after = after


def installed_apps() -> List[str]:
    return ["djp"] + list(itertools.chain(*pm.hook.installed_apps()))


def staticfiles_dirs() -> List[str]:
    return list(itertools.chain(*pm.hook.staticfiles_dirs()))


def staticfiles_finders() -> List[str]:
    return list(itertools.chain(*pm.hook.staticfiles_finders()))


def authentication_backends() -> List[str]:
    return list(itertools.chain(*pm.hook.authentication_backends()))


def auth_password_validators() -> List[str]:
    return list(itertools.chain(*pm.hook.auth_password_validators()))


def databases() -> dict:
    dict_list = pm.hook.databases()
    
    merged_dict = {}
    
    for dict_item in dict_list:
        merged_dict.update(dict_item)
        
    return merged_dict

def admin_sidebar_items() -> dict:
    dict_list = pm.hook.admin_sidebar_items()
    
    merged_dict = {}
    
    for dict_item in dict_list:
        merged_dict.update(dict_item)
    
    return merged_dict


def middleware(current_middleware: List[str]):
    before = []
    after = []
    default = []
    position_items = []

    for batch in pm.hook.middleware():
        for item in batch:
            if isinstance(item, Before):
                before.append(item.item)
            elif isinstance(item, After):
                after.append(item.item)
            elif isinstance(item, Position):
                position_items.append(item)
            elif isinstance(item, str):
                default.append(item)
            else:
                raise ValueError(f"Invalid item in middleware hook: {item}")

    combined = before + to_list(current_middleware) + default + after

    # Handle Position items
    for item in position_items:
        if item.before:
            try:
                idx = combined.index(item.before)
                combined.insert(idx, item.item)
            except ValueError:
                raise ValueError(f"Cannot find item to insert before: {item.before}")
        elif item.after:
            try:
                idx = combined.index(item.after)
                combined.insert(idx + 1, item.item)
            except ValueError:
                raise ValueError(f"Cannot find item to insert after: {item.after}")

    return combined


def urlpatterns():
    return list(itertools.chain(*pm.hook.urlpatterns()))


def context_processors():
    return list(itertools.chain(*pm.hook.context_processors()))


def builtins():
    return list(itertools.chain(*pm.hook.builtins()))

"""
def loaders():
    return list(itertools.chain(*pm.hook.loaders()))
"""

def settings(current_settings):
    # First wrap INSTALLED_APPS
    installed_apps_ = to_list(current_settings["INSTALLED_APPS"])
    installed_apps_ += installed_apps()
    current_settings["INSTALLED_APPS"] = installed_apps_
    
    # Now MIDDLEWARE
    current_settings["MIDDLEWARE"] = middleware(current_settings["MIDDLEWARE"])
    
    # Now DATABASES
    if setting_exists("DATABASES", current_settings):
        databases_ = databases()
        current_settings["DATABASES"].update(databases_)

    if setting_exists("CONTEXT_PROCESSORS", current_settings):
        # Now CONTEXT PROCESSORS
        context_processors_ = to_list(
            current_settings["TEMPLATES"][0]["OPTIONS"]["context_processors"]
        )
        context_processors_ += context_processors()
        current_settings["TEMPLATES"][0]["OPTIONS"]["context_processors"] = context_processors_
        
    if setting_exists("BUILTINS", current_settings):
        # Now BUILTINS
        builtins_ = to_list(
            current_settings["TEMPLATES"][0]["OPTIONS"]["builtins"]
        )
        builtins_ += builtins()
        current_settings["TEMPLATES"][0]["OPTIONS"]["builtins"] = builtins_
    
    """if setting_exists("LOADERS", current_settings):
        # Now LOADERS
        loaders_ = to_list(
            current_settings["TEMPLATES"][0]["OPTIONS"]["loaders"]
        )
        loaders_ += loaders()
        current_settings["TEMPLATES"][0]["OPTIONS"]["loaders"] = loaders_
    """
    
    if setting_exists("STATICFILES_DIRS", current_settings):
        # Now STATICFILES_FINDERS
        staticfiles_dirs_ = to_list(current_settings["STATICFILES_DIRS"])
        staticfiles_dirs_ += staticfiles_dirs()
        current_settings["STATICFILES_DIRS"] = staticfiles_dirs_
    
    if setting_exists("STATICFILES_FINDERS", current_settings):    
        # Now STATICFILES_DIRS
        staticfiles_finders_ = to_list(current_settings["STATICFILES_FINDERS"])
        staticfiles_finders_ += staticfiles_finders()
        current_settings["STATICFILES_FINDERS"] = staticfiles_finders_
    
    if setting_exists("AUTH_PASSWORD_VALIDATORS", current_settings):
        # Now AUTHPASSWORD_VALIDATORS    
        authpassword_validators_ = to_list(current_settings["AUTH_PASSWORD_VALIDATORS"])
        authpassword_validators_ += auth_password_validators()
        current_settings["AUTH_PASSWORD_VALIDATORS"] = authpassword_validators_
    
    if setting_exists("AUTHENTICATION_BACKENDS", current_settings):        
        # Now AUTHENTICATION_BACKENDS    
        authentication_backends_ = to_list(current_settings["AUTHENTICATION_BACKENDS"])
        authentication_backends_ += authentication_backends()
        current_settings["AUTHENTICATION_BACKENDS"] = authentication_backends_
    
    # Now apply any other settings() hooks
    pm.hook.settings(current_settings=current_settings)


def get_plugins():
    plugins = []
    plugin_to_distinfo = dict(pm.list_plugin_distinfo())
    for plugin in pm.get_plugins():
        plugin_info = {
            "name": plugin.__name__,
            "hooks": [h.name for h in pm.get_hookcallers(plugin)],
        }
        distinfo = plugin_to_distinfo.get(plugin)
        if distinfo:
            plugin_info["version"] = distinfo.version
            plugin_info["name"] = (
                getattr(distinfo, "name", None) or distinfo.project_name
            )
        plugins.append(plugin_info)
    return plugins


def to_list(tuple_or_list):
    if isinstance(tuple_or_list, tuple):
        return list(tuple_or_list)
    return tuple_or_list


def asgi_wrapper(application):
    for wrapper in pm.hook.asgi_wrapper():
        application = wrapper(application)
    return application


def check_if_settings_hook_target_exists():
    pass