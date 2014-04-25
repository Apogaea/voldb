import os

from volunteer.settings import *  # NOQA

import herokuify

from herokuify.common import *  # NOQA
from herokuify.aws import *  # NOQA

from volunteer.settings_aws import *  # NOQA

DATABASES = herokuify.get_db_config()
CACHES = herokuify.get_cache_config()

# Transactional requests
DATABASES['default']['ATOMIC_REQUESTS'] = True

DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'
TEMPLATE_DEBUG = DEBUG

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
