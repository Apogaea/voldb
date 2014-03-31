"""
Amazon Web Services

Requires:
    - herokuify
    - django-compressor
"""
import os

PROJECT_PATH = os.path.dirname(__file__)

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

DEFAULT_FILE_STORAGE = "herokuify.storage.S3MediaStorage"
MEDIA_URL = "https://{0}.s3.amazonaws.com/media/".format(AWS_STORAGE_BUCKET_NAME)

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

STATICFILES_STORAGE = "herokuify.storage.S3StaticStorage"
STATIC_URL = "https://{0}.s3.amazonaws.com/static/".format(AWS_STORAGE_BUCKET_NAME)

AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
