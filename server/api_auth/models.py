from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    user = models.OneToOneField(User)
    favorite_radio_shows = models.ManyToManyField('radio.RadioShow')
    favorite_news_shows = models.ManyToManyField('radio.NewsShow')
