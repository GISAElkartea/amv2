import os

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings


class Command(BaseCommand):
    help = 'Uploads the cors.xml file to the file storage'

    def handle(self, *args, **kwargs):
        filepath = os.path.join(settings.BASE_DIR, 'antxetamedia/heroku/cors.xml')
        with open(filepath) as c:
            cors = c.read()
        key = default_storage.bucket.new_key('cors')
        key.set_contents_from_string(cors)
