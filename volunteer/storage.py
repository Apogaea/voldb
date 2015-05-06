from django.contrib.staticfiles.storage import ManifestFilesMixin

from pipeline.storage import PipelineMixin

from s3_folder_storage.s3 import StaticStorage


class S3PipelineStorage(PipelineMixin, ManifestFilesMixin, StaticStorage):
    pass
