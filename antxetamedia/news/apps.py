from django.apps import AppConfig

from antxetamedia import archive


class NewsConfig(AppConfig):
    name = 'antxetamedia.news'

    def ready(self):
        archive.register(self.get_model('NewsCategory'))
        archive.register(self.get_model('NewsShow'))
        archive.register(self.get_model('NewsPodcast').objects.published())
