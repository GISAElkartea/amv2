from django.apps import AppConfig

import watson


class NewsConfig(AppConfig):
    name = 'antxetamedia.news'

    def ready(self):
        watson.register(self.get_model('NewsCategory'))
        watson.register(self.get_model('NewsShow'))
        watson.register(self.get_model('NewsPodcast').objects.published())
