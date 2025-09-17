from pathlib import Path
import os
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-change-me'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.staticfiles",
    'services',
    'bookings',
    'payments',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'booking.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'booking.wsgi.application'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
# If you keep a project-level static/ folder:
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = [ BASE_DIR / "static" ]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LOGIN_REDIRECT_URL = 'service_list'
LOGOUT_REDIRECT_URL = 'service_list'
