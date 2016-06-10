import traceback

from django.core.management.base import BaseCommand

from antxetamedia.blobs.models import Blob
from antxetamedia.blobs.tasks import update_blob


class Command(BaseCommand):
    help = 'Uploads blobs with local data to Archive.org'

    def handle(self, *args, **kwargs):
        for blob in Blob.objects.filter(local__isnull=False).exclude(local=''):
            result = update_blob.apply([blob.pk])
            if result.successful():
                self.stdout.write("Blob {} with ID {} has been uploaded successfully.\n".format(
                    blob, blob.pk))
            else:
                self.stderr.write("Exception while uploading blob {} with ID {}:\n{}\n".format(
                    blob, blob.pk, result.traceback))
