from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", False)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # 3rd party
    "nested_inline",
    "debug_toolbar",
    # local app
    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 3rd party
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DB_HOST = os.environ.get("DB_HOST", None)
if DB_HOST:
    DATABASES = {
        "default": {   
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': DB_HOST,
            'NAME': os.environ.get("POSTGRES_DB"),
            'USER': os.environ.get("POSTGRES_USER"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "th"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# where to store
MEDIA_ROOT = "/vol/web/media"
STATIC_ROOT = "/vol/web/static"
# STATIC_ROOT = BASE_DIR / "static"
# MEDIA_ROOT = BASE_DIR / "media"

# python manage.py collectstatic
STATICFILES_DIRS = [BASE_DIR / "app" / "mystatic"]

# LOGIN
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/profile"

# for debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# CUSTOM USER
AUTH_USER_MODEL = "core.User"

# MESSAGES
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}