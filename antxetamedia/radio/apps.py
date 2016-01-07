from django.apps import AppConfig


class RadioConfig(AppConfig):
    name = 'antxetamedia.radio'

    def ready(self):
        from antxetamedia.archive import adaptor
        adaptor.register(self.get_model('RadioProducer'))
        adaptor.register(self.get_model('RadioCategory'))
        adaptor.register(self.get_model('RadioShow'))
        adaptor.register(self.get_model('RadioPodcast').objects.published())
