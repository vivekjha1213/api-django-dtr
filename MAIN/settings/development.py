
import os
from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "django-insecure-key&2z!x5fequ-qc2hm*#akrkst52al*g==0n&n#d&m27"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "u714077623_stagedb",
#         "USER": "u714077623_stagedb",
#         "PASSWORD": "zVaUCU^6Ex@",
#         "HOST": "217.21.88.8", 
#         "PORT": "3306",  
#     }
# }

# logger: config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
           "filename": "dev-logs/debug.log",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    },
}


INTERNAL_IPS = [
    '127.0.0.1',
]



CORS_ALLOW_ALL_ORIGINS = True