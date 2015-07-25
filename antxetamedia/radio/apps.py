from django.apps import AppConfig

import watson


class RadioConfig(AppConfig):
    name = 'antxetamedia.radio'

    def ready(self):
        watson.register(self.get_model('RadioProducer'))
        watson.register(self.get_model('RadioCategory'))
        watson.register(self.get_model('RadioShow'))
        watson.register(self.get_model('RadioPodcast').objects.published())
