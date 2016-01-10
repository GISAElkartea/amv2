import os

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage


class Command(BaseCommand):
    help = 'Gives public read permissions'

    def handle(self, *args, **kwargs):
        default_storage.bucket.set_acl('public-read')
