from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from pipeline.storage import PipelineMixin

from s3_folder_storage.s3 import StaticStorage


class S3PipelineStorage(PipelineMixin, ManifestStaticFilesStorage, StaticStorage):
    pass
