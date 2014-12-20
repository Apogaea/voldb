"""
Django settings for volunteer project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import excavator

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = excavator.env_string('DJANGO_SECRET_KEY', required=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = excavator.env_bool('DJANGO_DEBUG', default=True)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = excavator.env_list('DJANGO_ALLOWED_HOSTS', required=not DEBUG)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # third party
    'authtools',
    'backupdb',
    'betterforms',
    'emailtools',
    'rest_framework',
    'compressor',
    'raven.contrib.django.raven_compat',
    # local project
    'volunteer',
    # local apps
    'departments',
    'shifts',
    'accounts',
    'profiles',
    # django admin
    'django.contrib.admin.apps.AdminConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'volunteer.urls'

WSGI_APPLICATION = 'volunteer.wsgi.application'

LOGIN_REDIRECT_URL = 'profile'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
import herokuify

DATABASES = herokuify.get_db_config()
DATABASES['default'].setdefault('ATOMIC_REQUESTS', True)

CACHES = herokuify.get_cache_config()

TEMPLATE_DEBUG = DEBUG

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static Files
STATIC_URL = excavator.env_string('DJANGO_STATIC_URL', default='/static/')
STATIC_ROOT = excavator.env_string(
    'DJANGO_STATIC_ROOT',
    default=os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = excavator.env_string('DJANGO_MEDIA_URL', default='/media/')
MEDIA_ROOT = excavator.env_string(
    'DJANGO_MEDIA_ROOT',
    default=os.path.join(BASE_DIR, 'media'),
)

DEFAULT_FILE_STORAGE = excavator.env_string(
    "DJANGO_DEFAULT_FILE_STORAGE",
    default="django.core.files.storage.FileSystemStorage",
)
STATICFILES_STORAGE = excavator.env_string(
    "DJANGO_STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.StaticFilesStorage"
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'volunteer', 'public'),
)

# Adding Auth Tools
# http://django-authtools.readthedocs.org/en/latest/intro.html#quick-setup
AUTH_USER_MODEL = 'accounts.User'

# Email Settings
EMAIL_LAYOUT = 'mail/base.html'
EMAIL_BACKEND = excavator.env_string(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = excavator.env_string('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = excavator.env_string('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = excavator.env_string('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = excavator.env_string('EMAIL_PORT', default='25')
EMAIL_USE_TLS = excavator.env_bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = excavator.env_bool('EMAIL_USE_SSL')

# `django.contrib.sites` settings
SITE_ID = 1

# django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_ujson.renderers.UJSONRenderer',
    ),
    # Pagination
    'PAGINATE_BY': 100,
    'MAX_PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size',
}


# Should users be allowed to register
REGISTRATION_OPEN = os.environ.get('REGISTRATION_OPEN', 'True') == 'True'

# Sentry
RAVEN_CONFIG = {
    'dsn': excavator.env_string('SENTRY_DSN', default=None),
}

# Herokuify
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# AWS
AWS_ACCESS_KEY_ID = excavator.env_string('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = excavator.env_string('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = excavator.env_string('AWS_STORAGE_BUCKET_NAME')

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

if not DEBUG:
    # Cached template loading is bad for dev so keep it off when debug is on.
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
