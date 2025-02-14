import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "your-django-secret-key")

# Debug Mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "backend-service",
        "backend-service.default.svc.cluster.local",
        "a4db59dda552049758b4e2cb631de79d-1080103396.us-east-1.elb.amazonaws.com",
        "a50ec3b714a554d65a17dbcd37703451-475530952.us-east-1.elb.amazonaws.com",
    ]

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "api",
    "api.user",
    "api.authentication",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS MUST be first!
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL Configuration
ROOT_URLCONF = "core.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# WSGI Application
WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("SQL_DATABASE", "django_db"),
        "USER": os.getenv("SQL_USER", "admin"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "supersecret"),
        "HOST": os.getenv("SQL_HOST", "postgres-service"),
        "PORT": os.getenv("SQL_PORT", "5432"),
    }
}

# Authentication User Model
AUTH_USER_MODEL = "api_user.User"

# REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "api.authentication.backends.ActiveSessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == [""]:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://a4db59dda552049758b4e2cb631de79d-1080103396.us-east-1.elb.amazonaws.com",
        "http://a50ec3b714a554d65a17dbcd37703451-475530952.us-east-1.elb.amazonaws.com",
    ]

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins (Allow API calls from frontend)
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Static & Media Files
STATIC_URL = "/api_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/api_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
