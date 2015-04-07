"""
Django settings for volunteer project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import excavator
import dj_database_url
import django_cache_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = excavator.env_string('DJANGO_SECRET_KEY', required=True)


ADMINS = (
    ('Piper', 'piper@apogaea.com.com'),
)

DEFAULT_FROM_EMAIL = excavator.env_string(
    'DJANGO_DEFAULT_FROM_EMAIL', default='volunteers@apogaea.com',
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = excavator.env_bool('DJANGO_DEBUG', default=False)

TEMPLATE_DEBUG = DEBUG

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'volunteer.core.context_processors.rollbar',
)

# Allowed Hosts
# https://docs.djangoproject.com/en/1.7/ref/settings/#allowed-hosts
ALLOWED_HOSTS = excavator.env_list('DJANGO_ALLOWED_HOSTS', required=not DEBUG)

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # local project
    'volunteer.core',
    # local apps
    'volunteer.apps.events',
    'volunteer.apps.departments',
    'volunteer.apps.shifts',
    'volunteer.apps.accounts',
    'volunteer.apps.profiles',

    # third party
    'authtools',
    'backupdb',
    'betterforms',
    'emailtools',
    'rest_framework',
    'pipeline',
    'manifesto',
    's3_folder_storage',
    'bootstrap3',
    'argonauts',
    'django_tables2',
]

try:
    # Error reporting client for Sentry
    import raven  # NOQA
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

    RAVEN_CONFIG = {
        'dsn': excavator.env_string('SENTRY_DSN', default=None)
    }
except ImportError:
    pass


if DEBUG:
    # Django Extensions
    # Provides useful tools for develpoment.
    try:
        import django_extensions  # NOQA
        INSTALLED_APPS.append('django_extensions')
    except ImportError:
        pass
    # Django Debug Toolbar
    # Provides useful tools for debugging sites either in development or
    # production.
    try:
        import debug_toolbar  # NOQA
        INSTALLED_APPS.append('debug_toolbar')
    except ImportError:
        pass

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Rollbar
# https://rollbar.com/
try:
    import rollbar  # NOQA
    MIDDLEWARE_CLASSES.append('rollbar.contrib.django.middleware.RollbarNotifierMiddleware')

    ROLLBAR = {
        'access_token': excavator.env_string('ROLLBAR_ACCESS_TOKEN', default=None),
        'environment': excavator.env_string('ROLLBAR_ENVIRONMENT', default='development'),
        'branch': excavator.env_string('ROLLBAR_GIT_BRANCH', default='master'),
        'root': BASE_DIR,
    }
except ImportError:
    pass

ROOT_URLCONF = 'volunteer.urls'

WSGI_APPLICATION = 'volunteer.wsgi.application'

LOGIN_REDIRECT_URL = 'dashboard'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.parse(excavator.env_string('DATABASE_URL', required=True)),
}
DATABASES['default'].setdefault('ATOMIC_REQUESTS', True)

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST7MDT'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Template Locations
# https://docs.djangoproject.com/en/1.7/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'volunteer', 'templates'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
DEFAULT_FILE_STORAGE = excavator.env_string(
    'DJANGO_DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage',
)
STATICFILES_STORAGE = excavator.env_string(
    'DJANGO_STATICFILES_STORAGE',
    default='django.contrib.staticfiles.storage.StaticFilesStorage',
)

# User-uploaded files
MEDIA_ROOT = excavator.env_string('DJANGO_MEDIA_ROOT')
MEDIA_URL = excavator.env_string('DJANGO_MEDIA_URL', default='/media/')

# Static files
STATIC_ROOT = excavator.env_string('DJANGO_STATIC_ROOT')
STATIC_URL = excavator.env_string('DJANGO_STATIC_URL', default='/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'volunteer', 'static'),
)

# Static file finders.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Django Pipeline Settings
PIPELINE_DISABLE_WRAPPER = excavator.env_bool(
    'DJANGO_PIPELINE_DISABLE_WRAPPER', default=True,
)
PIPELINE_ENABLED = excavator.env_bool('DJANGO_PIPELINE_ENABLED', not DEBUG)
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            "css/bootstrap.css",
            "css/bootstrap-black.css",
            "css/volunteer.css",
        ),
        'output_filename': 'css/base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            "js/jquery.js",
            "js/jquery.djangoCSRF.js",
            "js/moment-with-locales.js",
            "js/bootstrap.js",
            "js/json2.js",
            "js/underscore.js",
            "js/underscore.mixins.js",
            "js/handlebars.js",
            "js/backbone.js",
            "js/backbone.wreqr.js",
            "js/backbone.babysitter.js",
            "js/backbone.marionette.js",
            "js/backbone.marionette.export.js",
            "js/volunteer.js",
        ),
        'output_filename': 'base.js',
    },
    'shift-grid': {
        'source_filenames': (
            "js/shift-grid/templates/**.handlebars",
            "js/shift-grid/models.js",
            "js/shift-grid/collections.js",
            "js/shift-grid/views.js",
            "js/shift-grid/layouts.js",
            "js/shift-grid/app.js",
        ),
        'output_filename': 'js/shift-grid.js',
    },
}
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

PIPELINE_TEMPLATE_EXT = '.handlebars'
PIPELINE_TEMPLATE_FUNC = 'Handlebars.compile'
PIPELINE_TEMPLATE_NAMESPACE = 'Handlebars.templates'

# Custome User Model
# http://django-authtools.readthedocs.org/en/latest/intro.html#quick-setup
AUTH_USER_MODEL = 'accounts.User'


# Email Settings
EMAIL_LAYOUT = 'mail/base.html'
EMAIL_BACKEND = excavator.env_string(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = excavator.env_string('EMAIL_HOST')
EMAIL_HOST_USER = excavator.env_string('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = excavator.env_string('EMAIL_HOST_PASSWORD')
EMAIL_PORT = excavator.env_string('EMAIL_PORT', default='25')
EMAIL_USE_TLS = excavator.env_bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = excavator.env_bool('EMAIL_USE_SSL', default=True)

# AWS Config
AWS_ACCESS_KEY_ID = excavator.env_string('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = excavator.env_string('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = excavator.env_string('AWS_STORAGE_BUCKET_NAME', default=None)

DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

# Boto config
AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

# Cache setup
CACHES = {
    'default': django_cache_url.config(),
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# `django.contrib.sites` settings
SITE_ID = excavator.env_int('DJANGO_SITE_ID', default=1)

# Event ID
# - Designates the ID of the `active` event.
CURRENT_EVENT_ID = excavator.env_int("CURRENT_EVENT_ID", default=0) or None

# django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_ujson.renderers.UJSONRenderer',
    ),
    # Make test client always return json
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # Pagination
    'PAGINATE_BY': 100,
    'MAX_PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size',
}

REGISTRATION_OPEN = excavator.env_bool('REGISTRATION_OPEN', default=True)

if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
