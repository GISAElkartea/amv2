from django.apps import AppConfig

from antxetamedia import archive


class RadioConfig(AppConfig):
    name = 'antxetamedia.radio'

    def ready(self):
        archive.register(self.get_model('RadioProducer'))
        archive.register(self.get_model('RadioCategory'))
        archive.register(self.get_model('RadioShow'))
        archive.register(self.get_model('RadioPodcast').objects.published())
