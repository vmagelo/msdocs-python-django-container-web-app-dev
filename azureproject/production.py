import os
from .settings import *

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# MongoDB used.
DATABASES = {}

