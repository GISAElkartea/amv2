from django.apps import AppConfig

from antxetamedia import archive


class EventsConfig(AppConfig):
    name = 'antxetamedia.events'

    def ready(self):
        archive.register(self.get_model('Event'))
