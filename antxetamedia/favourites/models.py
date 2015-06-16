from django.db import models
from django.conf import settings


class FavouriteNewsShow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    show = models.ForeignKey('news.newsshow')


class FavouriteRadioShow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    show = models.ForeignKey('radio.radioshow')
