import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost','127.0.0.1','54.184.142.184']

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
