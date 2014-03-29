import os

from volunteer.settings import *  # NOQA

import herokuify

from herokuify.common import *  # NOQA
from herokuify.aws import *  # NOQA

from volunteer.settings_aws import *  # NOQA

DATABASES = herokuify.get_db_config()
CACHES = herokuify.get_cache_config()

DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'
TEMPLATE_DEBUG = DEBUG
