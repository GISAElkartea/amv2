from django.core.signals import post_save
from django.dispatch import receiver

from .models import Blob, BlobUpload


@receiver(post_save, sender=Blob)
def upload_blobs(sender, instance, **kwargs):
    # TODO: All this needs to be moved into a celery task
    if instance.local is not None:
        upload = BlobUpload.objects.create(blob=instance)
        upload.upload()
