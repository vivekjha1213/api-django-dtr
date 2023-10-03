from .base import *

# Secret key (change this in production, use environment variable)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "sfdfghjklmkmdnu%%vgq123091hokeee~120831-?--/")

# Disable debugging in production
DEBUG = False

# Define the allowed hostnames for your production server
ALLOWED_HOSTS = ["your-production-domain.com", "www.your-production-domain.com"]

# Configure your production database here (e.g., PostgreSQL or MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Choose your database engine
        "NAME": "your_database_name",
        "USER": "your_database_user",
        "PASSWORD": "your_database_password",
        "HOST": "your_database_host",  # Change this to your actual MySQL host
        "PORT": "your_database_port",  # Change this to your actual MySQL port
    }
}


