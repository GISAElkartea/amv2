from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'antxetamedia.news'

    def ready(self):
        from antxetamedia.archive import adaptor
        adaptor.register(self.get_model('NewsCategory'))
        adaptor.register(self.get_model('NewsShow'))
        adaptor.register(self.get_model('NewsPodcast').objects.published())
