import traceback

from django.db.models.signals import post_save
from django.conf import settings

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
        update_blob.apply_async([instance], retry_policy=RETRY_POLICY)


def queue_podcast_update(sender, instance, **kwargs):
    for blob in instance.blob_set.iterator():
        update_blob.apply_async([blob], retry_policy=RETRY_POLICY)


if getattr(settings, 'SYNC_BLOBS', False):
    post_save.connect(queue_blob_upload, sender=Blob)
    for subclass in AbstractPodcast.__subclasses__():
        post_save.connect(queue_podcast_update, sender=subclass)


@shared_task
def update_blob(blob):
    upload = BlobUpload.objects.create(blob=blob)
    upload.is_uploading()
    try:
        connection = ArchiveS3(blob.account)
        connection.create_or_update_bucket(blob.content_object)
        key = connection.get_or_create_key(blob)
        if blob.local:
            key.set_contents_from_file(blob.local.file)
        url = connection.build_url(blob)
    except Exception:
        upload.is_unsuccessful(traceback.format_exc())
    else:
        upload.is_successful(url)
