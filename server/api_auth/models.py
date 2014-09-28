from django.db import models

from custom_user.models import AbstractEmailUser


class APIUser(AbstractEmailUser):
    favorite_radio_shows = models.ManyToManyField('radio.RadioShow')
    favorite_news_shows = models.ManyToManyField('radio.NewsShow')