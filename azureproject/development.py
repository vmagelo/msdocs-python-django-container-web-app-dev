import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Don't use Whitenoise to avoid having to run collectstatic first.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ALLOWED_HOSTS = ['*']

# MongoDB used.
DATABASES = {}
