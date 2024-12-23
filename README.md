# DJP: Django Plugins

[![PyPI](https://img.shields.io/pypi/v/djp.svg)](https://pypi.org/project/djp/)
[![Tests](https://github.com/simonw/djp/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/djp/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/djp?include_prereleases&label=changelog)](https://github.com/simonw/djp/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/djp/blob/main/LICENSE)

A plugin system for Django

Visit **[djp.readthedocs.io](https://djp.readthedocs.io/)** for full documentation, including how to install plugins and how to write new plugins.

See [DJP: A plugin system for Django](https://simonwillison.net/2024/Sep/25/djp-a-plugin-system-for-django/) for an introduction to this project.

## Installation

Install this library using `pip`:
```bash
pip install djp
```

## Configuration

Add this to the **end** of your `settings.py` file:
```python
import djp

# ... existing settings.py contents

djp.settings(globals())
```
Then add this to your URL configuration in `urls.py`:
```python
urlpatterns = [
    # ...
] + djp.urlpatterns()
```

## Usage

Installing a plugin in the same environment as your Django application should cause that plugin to automatically add the necessary 

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd djp
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

# Notes: (Lusayo - 12 December 2024):
Here are the changes I've made to DJP that justify forking it as an experimental repo:

1. Added extra hooks for hooking into different parts of the config:

- databases
    - This adds to the project's DATABASES setting. Unvalidated as of now.
- context_processors
    - This adds to the project's context_processors option for the first templating engine found inside the TEMPLATES setting. Note it only adds context_processors to the first dictionary found inside the TEMPLATES setting.
- builtins
    - This adds to the project's builtins option for the first templating engine found inside the TEMPLATES setting. Note it only adds the builtins to the first dictionary found inside the TEMPLATES setting.
- staticfiles_dirs
    - This adds to the project's STATICFILES_DIRS setting if present in the project.
- staticfiles_finders
    - This adds to the project's STATICFILES_FINDERS setting if present in the project.
- authentication_backends
    - This adds to the project's AUTHENTICATION_BACKENDS setting if present in the project.
- auth_password_validators
    - This adds to the project's AUTH_PASSWORD_VALIDATORS setting if present in the project.
- page_head_includes
    - This works together with the {% djp_page_head_includes %} template tag, registering whatever string is included as part of the output of that tag.
- page_body_includes
    - This works together with the {% djp_page_body_includes %} template tag, registering whatever string is included as part of the output of that tag.

* NOTE: I played around with also allowing a "loaders" hook for the templating engine options, but I think adding that hook is going to complicate things, so I've put it off for now.

2. Added a custom management command for showing the current value of the DJP_PLUGINS_DIR setting. This is useful for adding plugins to django projects on the fly.