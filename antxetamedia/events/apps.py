from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'antxetamedia.events'

    def ready(self):
        from antxetamedia.archive import adaptor
        adaptor.register(self.get_model('Event'))
