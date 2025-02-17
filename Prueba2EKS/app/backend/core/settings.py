import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "your-django-secret-key")

# Debug Mode (Ensures it's a boolean)
DEBUG = os.getenv("DEBUG", "False").strip().lower() in ("true", "1", "yes")

# Allowed Hosts (Ensures Proper Splitting & Default Values)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").replace(" ", "").split(",")

# Default Allowed Hosts if empty or misconfigured
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "backend-service",
        "backend-service.default.svc.cluster.local",
        "aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com",
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

# Middleware (CORS Middleware MUST be first)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
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

# Database Configuration
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


CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").replace(" ", "").split(",")

if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == [""]:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://a1ea82fa5c25a46e4a572f1871350ccb-1392024633.us-east-1.elb.amazonaws.com",
    ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]


CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Static & Media Files
STATIC_URL = "/api_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/api_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
