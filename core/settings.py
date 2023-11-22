import os
from decouple import config
from django.core.exceptions import ImproperlyConfigured

if config('MODE') == 'Dev':
    try:
        from .settings.development import * 
    except ImportError:
        raise ImproperlyConfigured("Development settings not found")
    
elif config('MODE') == 'PRODUCTION':
    try:
        from settings.production import *  
    except ImportError:
        raise ImproperlyConfigured("Development settings not found")
    
