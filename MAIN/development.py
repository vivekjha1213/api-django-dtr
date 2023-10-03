from settings.base import *


DEBUG = True



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Enable Django Debug Toolbar for development
INSTALLED_APPS += [
    'debug_toolbar',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

# Allow localhost for Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]



# CORS settings for development (allow all origins)
CORS_ALLOW_ALL_ORIGINS = True

# Set up logging for development (customize as needed)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
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
            "handlers": ["debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
