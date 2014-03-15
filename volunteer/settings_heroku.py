import os

from volunteer.settings import *  # NOQA

import herokuify

from herokuify.common import *  # NOQA
from herokuify.aws import *  # NOQA

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = herokuify.get_db_config()
CACHES = herokuify.get_cache_config()

DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'
TEMPLATE_DEBUG = DEBUG
