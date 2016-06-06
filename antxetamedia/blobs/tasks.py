import traceback

from django.db.models.signals import post_save
from django.conf import settings
from django.core.files.storage import default_storage

from celery import shared_task

from ..shows.models import AbstractPodcast
from .models import Blob, BlobUpload
from .archive import ArchiveS3


RETRY_POLICY = {
    'max_retries': 5,
    'interval_start': 0,
    'interval_step': 5*60,
    'interval_max': 60*60,
}


def queue_blob_upload(sender, instance, **kwargs):
    if instance.local:  # Only sync if there is something to upload
        update_blob.apply_async([instance.pk], retry_policy=RETRY_POLICY)


def queue_podcast_update(sender, instance, **kwargs):
    for blob in instance.blob_set.iterator():
        update_blob.apply_async([blob.pk], retry_policy=RETRY_POLICY)


if getattr(settings, 'SYNC_BLOBS', False):
    post_save.connect(queue_blob_upload, sender=Blob)
    for subclass in AbstractPodcast.__subclasses__():
        post_save.connect(queue_podcast_update, sender=subclass)


@shared_task(bind=True)
def update_blob(self, blob_pk):
    try:
        blob = Blob.objects.get(pk=blob_pk)
    except Blob.DoesNotExist:
        return
    upload = BlobUpload.objects.create(blob=blob)
    upload.is_uploading()
    try:
        connection = ArchiveS3(blob.account)
        connection.create_or_update_bucket(blob.content_object)
        # Delete reference to a non-existent filed
        if blob.local and not default_storage.exists(blob.local.name):
            blob.local = None
        url = blob.remote
        if blob.local:
            key = connection.get_or_create_key(blob)
            key.set_contents_from_file(blob.local.file)
            url = connection.build_url(blob)
    except Exception as exc:
        upload.is_unsuccessful(traceback.format_exc())
        raise self.retry(exc=exc)
    else:
        upload.is_successful(url)
