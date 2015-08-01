try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
import traceback

from django.db.models.signals import post_save
from django.dispatch import receiver

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.exception import S3ResponseError
from celery import shared_task

from .models import Blob, BlobUpload


@receiver(post_save, sender=Blob)
def queue_blob_upload(sender, instance, **kwargs):
    upload_blob.apply_async([instance], retry_policy={
        'max_retries': 5,
        'interval_start': 0,
        'interval_step': 5*60,
        'interval_max': 60*60,
    })


@shared_task
def upload_blob(blob):
    if blob.local:
        upload = BlobUpload.objects.create(blob=blob)
        upload.is_uploading()

        try:
            # Create connection
            connection = S3Connection(blob.account.username, blob.account.password, is_secure=False,
                                      host='s3.us.archive.org', calling_format=OrdinaryCallingFormat())

            # Get or create bucket
            bucket = '{prefix}-{show}-{podcast}'.format(prefix=connection.access_key.lower(),
                                                        show=blob.content_object.show.slug.lower(),
                                                        podcast=blob.content_object.slug.lower())
            try:
                bucket = connection.get_bucket(bucket)
            except S3ResponseError as exp:
                if not exp.status == 404:
                    raise
                metadata = getattr(blob.content_object, 'metadata', {})
                bucket = connection.create_bucket(bucket, metadata=metadata)

            # Create key
            key = bucket.new_key(str(blob))  # Guaranteed to be unique

            # Upload contents
            key.set_contents_from_file(blob.local.file)

            # Build remote url
            url = 'https://archive.org/download/{bucket}/{key}'.format(bucket=quote(bucket.name), key=quote(key.key))
        except Exception as exp:
            upload.is_unsuccessful(traceback.format_exc())
        else:
            upload.is_successful(url)
