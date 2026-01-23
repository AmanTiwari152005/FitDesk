"""
Django settings for gym_management project.
Firebase-based authentication (NO allauth, NO dj-rest-auth)
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# BASIC CONFIG
# --------------------------------------------------

SECRET_KEY = "django-insecure-b1jn*$#8zzyz*ef42&%%*6sz_jgo(e@^89n8-=-xko=5u@ztc3"


DEBUG = True

ALLOWED_HOSTS = []


# --------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # DRF
    "rest_framework",
    "rest_framework.authtoken",

    # Your apps
    "accounts",
    "members",
    "gym",
    "expenses",
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# --------------------------------------------------
# URL / TEMPLATES
# --------------------------------------------------

ROOT_URLCONF = "gym_management.urls"

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

WSGI_APPLICATION = "gym_management.wsgi.application"

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gym_db',
        'USER': 'gym_user',
        'PASSWORD': 'gym123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}










# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = BASE_DIR / "staticfiles"



# --------------------------------------------------
# REST FRAMEWORK (TOKEN AUTH)
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
# AUTH BACKEND (DEFAULT ONLY)
# --------------------------------------------------

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ---------------- EMAIL CONFIG (GMAIL SMTP) ----------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "atiwary489@gmail.com"
EMAIL_HOST_PASSWORD = "gclujiyajdmzhtry"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


LOGIN_URL = "/api/accounts/login-page/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/api/accounts/login-page/"


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True







# --------------------------------------------------
# LOGIN / LOGOUT REDIRECTS
# --------------------------------------------------

# LOGIN_REDIRECT_URL = "/dashboard/"
# LOGOUT_REDIRECT_URL = "/api/accounts/login-page/"

# --------------------------------------------------
# IMPORTANT NOTES
# --------------------------------------------------
# ✔ django-allauth REMOVED
# ✔ dj-rest-auth REMOVED
# ✔ Firebase handles Google auth
# ✔ Django only verifies Firebase token



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}



