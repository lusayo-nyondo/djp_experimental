import djp

SECRET_KEY = "django-insecure-test-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
)

MIDDLEWARE: tuple = tuple()

ROOT_URLCONF = "tests.test_project.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [(
                'django.template.loaders.cached.Loader', [
                    # Default Django loader
                    'django.template.loaders.filesystem.Loader',
                    # Inluding this is the same as APP_DIRS=True
                    'django.template.loaders.app_directories.Loader',
                    # Components loader
                    'django_components.template_loader.Loader',
                ]
            )],
            'builtins': [
                'django_components.templatetags.component_tags',
                'themer.templatetags.themer_tags',
            ]
        },
    }
]

USE_TZ = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    "./"
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

djp.settings(globals())
