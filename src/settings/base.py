from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(env_file=str(BASE_DIR / ".env"))

SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

INSTALLED_APPS = [
    # channels
    # "channels",
    # django contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # 3rd party
    "nested_admin",
    "markdownx",
    # local app
    "core.apps.CoreConfig",
    "game.apps.GameConfig",
    "docker_instance.apps.DockerInstanceConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # whitenoise for static files
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "PORT": os.environ.get("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "th"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# where to store
MEDIA_ROOT =  "media"
STATIC_ROOT = "static"

STATICFILES_DIRS = [BASE_DIR / "app" / "static"]

# whitenoise cache static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# LOGIN
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/profile"


# CUSTOM USER
AUTH_USER_MODEL = "core.User"

# MESSAGES
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

WSGI_APPLICATION = "app.wsgi.application"
# ASGI_APPLICATION = 'app.asgi.application'

CSRF_COOKIE_HTTPONLY = False

# MARKDOWN X
MARKDOWNX_MARKDOWNIFY_FUNCTION = "markdownx.utils.markdownify"
MARKDOWNX_MARKDOWN_EXTENSIONS = (
    "pymdownx.extra",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.details",
    "pymdownx.saneheaders",
    "pymdownx.magiclink",
    "markdown.extensions.nl2br",
    "markdown.extensions.smarty",
    "markdown.extensions.sane_lists",
    "markdown_captions",
)

from pymdownx.superfences import fence_div_format

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    "pymdownx.extra": {
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "mermaid",
                    "class": "mermaid",
                    "format": fence_div_format,
                }
            ]
        }
    }
}

from datetime import datetime

MARKDOWNX_MEDIA_PATH = datetime.now().strftime("markdownx/%Y/%m/%d")

MARKDOWNX_IMAGE_MAX_SIZE = {
    'size': (500, 0),
    'quality': 100
}
