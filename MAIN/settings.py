import os
from datetime import timedelta


from pathlib import Path

import pymysql

pymysql.install_as_MySQLdb()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b&2z!x5fequ-qc2hm*czn04yj#akrkst52al*g==0n&n#d&m27"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# image and logo, config...

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "rest_framework_swagger",
    "drf_yasg",  # <-- Swagger-ui
    # Internal Apps,
    "Hospitals",
    "patients",
    "doctors",
    "Departments",
    "Nurses",
    "Medicines",
    "Appointments",
    "Beds",
    "Prescriptions",
    "PrescriptionDetails",
    "Invoices",
    "Payments",
    "LabTests",
    "feedbacks",
]


AUTH_USER_MODEL = "Hospitals.Hospital"


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Default Django backend
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "MAIN.urls"

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

WSGI_APPLICATION = "MAIN.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "u714077623_HMS_API_TEST",
        "USER": "u714077623_HMS_API_TEST",
        "PASSWORD": "n46Q@6&XLh3nd5N",
        "HOST": "217.21.88.8",  # Change if your MySQL server is running on a different host
        "PORT": "3306",  # Change if your MySQL server is running on a different port
    }
}


# SWAGGER_SETTINGS = {
#     "SECURITY_DEFINITIONS": {
#         "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
#     }
# }


SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
    'APIS_SORTER': 'alpha',
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {  # <<-- is for JWT access token
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'basic': {  # <<-- is for djagno authentication 
            'type': 'basic'
        },
    },
}


LOGIN_URL = 'http://127.0.0.1:8000/swagger/'






REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}


# Set the custom payload handler
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "client_id",  # Use your primary key field here
    "USER_ID_CLAIM": "client_id",  # Use your primary key field here
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


CORS_ALLOWED_ORIGINS = [
    "http://192.168.1.61:3000",  # -> ravi
    "http://194.163.40.231:8080",  # -> production
    "http://127.0.0.1:8000",  # -> local
    "http://172.20.10.11:3000",  # -> pragati
]

PASSWORD_RESET_TIMEOUT = 900  # 900 Sec = 15 Min


# logger: config
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "Debug_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/debug.log"),
#             "formatter": "verbose",
#         },
#         "auth_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/auth.log"),
#             "formatter": "verbose",
#         },
#         "doctor_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/doctor.log"),
#             "formatter": "verbose",
#         },
#         "patient_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/patient.log"),
#             "formatter": "verbose",
#         },
#         "booking_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/Appointment.log"),
#             "formatter": "verbose",
#         },
#         "BookingSlotAvailability_file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/BookingSlotAvailability.log"),
#             "formatter": "verbose",
#         },
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["Debug_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "account.auth": {
#             "handlers": ["auth_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "doctor.doctor": {
#             "handlers": ["doctor_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "patients.patient": {
#             "handlers": ["patient_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "appointment.booking": {
#             "handlers": ["booking_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "BookingSlotAvailability.BookingSlot": {
#             "handlers": ["BookingSlotAvailability_file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    },
}

# Email-Configuration......

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_USE_TLS = True



# EMAIL_HOST_USER = "vivek.jha@dtroffle.com" 
# EMAIL_HOST_PASSWORD = "gsyvamddfrpihzdo"