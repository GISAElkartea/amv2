from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'antxetamedia.projects'

    def ready(self):
        from antxetamedia.archive import adaptor
        adaptor.register(self.get_model('ProjectProducer'))
        adaptor.register(self.get_model('ProjectShow'))
        adaptor.register(self.get_model('ProjectPodcast').objects.published())
