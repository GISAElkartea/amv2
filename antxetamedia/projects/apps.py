from django.apps import AppConfig

from antxetamedia import archive


class ProjectsConfig(AppConfig):
    name = 'antxetamedia.projects'

    def ready(self):
        archive.register(self.get_model('ProjectProducer'))
        archive.register(self.get_model('ProjectShow'))
        archive.register(self.get_model('ProjectPodcast').objects.published())
