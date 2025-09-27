from pathlib import Path
import environ
import os
from datetime import timedelta  # ¡Importación necesaria para la configuración JWT!
import dj_database_url  # ← añade esto

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- Env ----------------
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
)
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

SECRET_KEY = env("SECRET_KEY", default="unsafe-dev-key")
DEBUG = env.bool("DEBUG", default=False)

# Producción: dominios Railway + Netlify + local
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[
    "backend-production-e5d6.up.railway.app",
    "localhost",
    "127.0.0.1",
])

# ---------------- Apps ----------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # terceros
    "rest_framework",
    "corsheaders",

    # tus apps
    "users",
    "products",
]

# ⚠️ Si tienes modelo custom de usuarios en users/models.py
AUTH_USER_MODEL = "users.User"

# ---------------- Middleware ----------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",         # ← PRIMERO
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"

# ---------------- Base de datos (SOLO Postgres) ----------------
# Requiere que exista DATABASE_URL; si falta, Django no arranca (como deseas)
DATABASE_URL = env("DATABASE_URL")  # levanta ImproperlyConfigured si no está definida

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=env.int("DB_CONN_MAX_AGE", default=600),
        ssl_require=True,  # fuerza SSL en producción
    )
}

# ---------------- DRF / Auth ----------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# ---------------- JWT ----------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",

    # Cookie de refresh (si la usas)
    "REFRESH_TOKEN_COOKIE_NAME": "refresh_token",
    "REFRESH_TOKEN_COOKIE_DOMAIN": None,
    "REFRESH_TOKEN_COOKIE_PATH": "/",
    "REFRESH_TOKEN_COOKIE_SECURE": not DEBUG,
    "REFRESH_TOKEN_COOKIE_HTTPONLY": True,
    "REFRESH_TOKEN_COOKIE_SAMESITE": "Lax",
}

# ---------------- i18n ----------------
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ---------------- Static ----------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------- CORS / CSRF ----------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[
    "https://iessence.netlify.app",
    "http://localhost:5173",
])
CORS_ALLOWED_ORIGIN_REGEXES = env.list("CORS_ALLOWED_ORIGIN_REGEXES", default=[
    r"^https:\/\/deploy-preview-\d+\.netlify\.app$",
])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[
    "https://iessence.netlify.app",
    "https://*.netlify.app",
    "https://backend-production-e5d6.up.railway.app",
])

# Detrás de proxy (Railway)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = not DEBUG
