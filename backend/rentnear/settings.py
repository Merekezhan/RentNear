
import os
from pathlib import Path

import dj_database_url

from rentnear.env import load_env

load_env()

# --------------------------------------------------
# Base configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get(
    "DJANGO_DEBUG", "true"
).lower() == "true"

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-rentnear-secret-key" if DEBUG else "",
)

if not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY must be set in production."
    )

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]

# Automatically allow the Render backend hostname
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)


# --------------------------------------------------
# Installed applications
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",

    "accounts",
    "marketplace",
    
    "cloudinary_storage",
    "cloudinary",
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------
# URLs and templates
# --------------------------------------------------

ROOT_URLCONF = "rentnear.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors",
            ],
        },
    },
]

# Use Django's standard messages context processor
TEMPLATES[0]["OPTIONS"]["context_processors"][-1] = (
    "django.contrib.messages.context_processors.messages"
)

WSGI_APPLICATION = "rentnear.wsgi.application"
ASGI_APPLICATION = "rentnear.asgi.application"


# --------------------------------------------------
# PostgreSQL database
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "rentnear"),
        "USER": os.environ.get("POSTGRES_USER", "rentnear"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Render supplies DATABASE_URL for cloud PostgreSQL.
# Local PostgreSQL continues to work without it.

if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=0,
        conn_health_checks=True,
    )


# --------------------------------------------------
# Custom user model
# --------------------------------------------------

AUTH_USER_MODEL = "accounts.User"


# --------------------------------------------------
# Password validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        )
    },
]


# --------------------------------------------------
# Language and timezone
# --------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# Static files (WhiteNoise)
# --------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
    "BACKEND": (
        "cloudinary_storage.storage.MediaCloudinaryStorage"
        if os.environ.get("CLOUDINARY_CLOUD_NAME")
        else "django.core.files.storage.FileSystemStorage"
    ),
},
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}



# --------------------------------------------------
# Uploaded media
# --------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# CORS (React frontend)
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ALLOWED_ORIGINS",
        (
            "http://localhost:5173,"
            "http://127.0.0.1:5173"
        ),
    ).split(",")
    if origin.strip()
]


# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# --------------------------------------------------
# Render production security
# --------------------------------------------------

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SECURE_SSL_REDIRECT = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# --------------------------------------------------
# Default primary key
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Log server errors to Render Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
