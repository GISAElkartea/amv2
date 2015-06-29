from django.apps import AppConfig


class BlobsConfig(AppConfig):
    name = 'antxetamedia.blobs'

    def ready(self):
        from . import tasks  # noqa
