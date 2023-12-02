import os
import pymysql

pymysql.install_as_MySQLdb()
from datetime import timedelta

# ...

# Secret key-(change this in production)
SECRET_KEY = "django-insecure-b&2z!x5fequ-qc2hm*czn04yj#akrkst52al*g==0n&n#d&m27"

# Build paths inside the project like this: BASE_DIR-/-'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")



DEBUG = True
ALLOWED_HOSTS = ['*']

# ...

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/



DEFAULT_APPS=[
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "django_filters",
    "rest_framework_swagger",
    "drf_yasg", 
    "django_extensions",
]

LOCAL_APPS = [
    "apps.Hospitals",
    "apps.patients",
    "apps.doctors",
    "apps.Departments",
    "apps.Nurses",
    "apps.Medicines",
    "apps.Appointments",
    "apps.Beds",
    "apps.Prescriptions",
    "apps.PrescriptionDetails",
    "apps.Invoices",
    "apps.Payments",
    "apps.LabTests",
    "apps.feedbacks",
    "apps.packages",
]
INSTALLED_APPS =DEFAULT_APPS+THIRD_PARTY_APPS +LOCAL_APPS

AUTH_USER_MODEL = "Hospitals.Hospital"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend", 
]
ROOT_URLCONF = "core.urls"
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
WSGI_APPLICATION = "core.wsgi.application"




DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u428490017_stagehub',
        'USER': 'u428490017_stagehub',
       'PASSWORD': '?aTJZZSL>0k',
        'HOST': '217.21.88.8', 
        'PORT': '3306',
	}
}


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }
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




# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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
    "apps.Middleware.UserAgent.CustomUserAgentMiddleware",
    "apps.Middleware.timing_middleware.TimingMiddleware",
    "apps.Middleware.rate_limit.RateLimitMiddleware",
    
]



''' 
# Celery config........
CELERY_BROKER_URL = "redis://127.0.0.1:6379"  # mac local, server air -> redis server
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

'''

SWAGGER_SETTINGS = {
    "DOC_EXPANSION": "list",
    "APIS_SORTER": "alpha",
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {  # <<-- is for JWT access token
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
        "basic": {"type": "basic"},  # <<-- is for djagno authentication
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
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
    "USER_ID_FIELD": "client_id",  #  primary key field here...
    "USER_ID_CLAIM": "client_id",  #  primary key field here.....
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

PASSWORD_RESET_TIMEOUT = 900  # 900 Sec = 15 Min


# Email-Configuration......
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_USE_TLS = True


# python3 manage.py runserver --settings=core.settings



# Secret key (change this in production, use environment variable)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "sfdfghjklmkmdnu%%vgq123091hokeee~120831-?--/")

# Disable debugging in production
DEBUG = False


ALLOWED_HOST = ['*']
# ALLOWED_HOSTS = ["iyrajewels.com", "www.iyrajewels.com", "194.163.40.231"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure  production database here (e.g., PostgreSQL or MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "u714077623_HMS_API_TEST",
        "USER": "u714077623_HMS_API_TEST",
        "PASSWORD": "n46Q@6&XLh3nd5N",
        "HOST": "217.21.88.8", 
        "PORT": "3306",  
    }
}


"""
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "Debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/api.log"),
            "formatter": "verbose",
        },
        "Hospital_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Hospitals.log"),
            "formatter": "verbose",
        },
        "doctor_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/doctors.log"),
            "formatter": "verbose",
        },
        "patient_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/patients.log"),
            "formatter": "verbose",
        },
        "booking_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Appointment.log"),
            "formatter": "verbose",
        },
        "Bed_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Beds.log"),
            "formatter": "verbose",
        },
        "feedbacks_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/feedbacks.log"),
            "formatter": "verbose",
        },
        "Medicines_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Medicines.log"),
            "formatter": "verbose",
        },
        "Nurses_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Nurses.log"),
            "formatter": "verbose",
        },
        "PrescriptionDetails_file": {  # Corrected handler name
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/PrescriptionDetails.log"),
            "formatter": "verbose",
        },
        "Prescriptions_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Prescriptions.log"),
            "formatter": "verbose",
        },
        "LabTest_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/LabTest.log"),
            "formatter": "verbose",
        },
        "Payment_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Payments.log"),
            "formatter": "verbose",
        },
        "Invoice_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Invoices.log"),
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["Debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "Hospitals.Hospital": {
            "handlers": ["Hospital_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "doctors.doctor": {
            "handlers": ["doctor_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "patients.patient": {
            "handlers": ["patient_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Appointments.Appointment": {
            "handlers": ["booking_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Beds.Bed": {
            "handlers": ["Bed_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "feedbacks.feedback": {
            "handlers": ["feedbacks_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Medicines.Medicine": {
            "handlers": ["Medicines_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Nurses.Nurse": {
            "handlers": ["Nurses_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "PrescriptionDetails.PrescriptionDetail": {  # Corrected logger name
            "handlers": ["PrescriptionDetails_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Prescriptions.Prescription": {
            "handlers": ["Prescriptions_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "LabTests.LabTest": {
            "handlers": ["LabTest_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Payments.Payment": {
            "handlers": ["Payment_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Invoices.Invoice": {
            "handlers": ["Invoice_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


 """
 
 

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
           "filename": "deb/debug.log",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    },
}
