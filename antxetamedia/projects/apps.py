from django.apps import AppConfig

import watson


class ProjectsConfig(AppConfig):
    name = 'antxetamedia.projects'

    def ready(self):
        watson.register(self.get_model('ProjectProducer'))
        watson.register(self.get_model('ProjectShow'))
        watson.register(self.get_model('ProjectPodcast').objects.published())
