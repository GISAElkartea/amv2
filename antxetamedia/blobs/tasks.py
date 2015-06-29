from urllib import quote

from django.db.models.signals import post_save
from django.dispatch import receiver

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.exception import S3ResponseError

from .models import Blob, BlobUpload


@receiver(post_save, sender=Blob)
def upload_blob(sender, instance, **kwargs):
    # TODO: All this needs to be moved into a celery task
    blob = instance
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
                bucket = connection.create_bucket(bucket)

            # Create key
            key = bucket.new_key(str(blob))

            # Upload contents
            key.set_contents_from_file(blob.local.file)

            # Build remote url
            #url = key.generate_url(expires_in=0, query_auth=False)
            url = 'https://archive.org/download/{bucket}/{key}'.format(bucket=quote(bucket.name), key=quote(key.key))
        except Exception as exp:
            upload.is_unsuccessful(exp)
        else:
            upload.is_successful(url)
