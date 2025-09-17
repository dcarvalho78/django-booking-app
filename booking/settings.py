from pathlib import Path
import os

# Basis
BASE_DIR = Path(__file__).resolve().parent.parent

# Sicherheit / Debug aus Umgebungsvariablen (für lokal okay)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Hosts (lokal ok; in Prod per Env setzen: DJANGO_ALLOWED_HOSTS="example.com,www.example.com")
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # deine Apps:
    "services",
    "bookings",
    "payments",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # <— statische Dateien in Prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "booking.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "booking.wsgi.application"

# Datenbank (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

# Locale
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"         # Ziel für collectstatic
STATICFILES_DIRS = [BASE_DIR / "static"]       # falls du ./static/ im Projekt nutzt
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Proxy/HTTPS (problemlos lokal; in Prod nützlich)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG

# Optional via Env: CSRF_TRUSTED_ORIGINS="https://example.com,https://www.example.com"
CSRF_TRUSTED_ORIGINS = [u for u in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if u]

# IDs
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Login-Redirects
LOGIN_REDIRECT_URL = "service_list"
LOGOUT_REDIRECT_URL = "service_list"
