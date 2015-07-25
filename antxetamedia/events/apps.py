from django.apps import AppConfig

import watson


class EventsConfig(AppConfig):
    name = 'antxetamedia.events'

    def ready(self):
        Event = self.get_model('Event')
        watson.register(Event)
