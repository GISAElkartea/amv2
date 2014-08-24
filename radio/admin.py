from django.contrib import admin

from .models import (NewsShow, RadioShow, ProjectShow,
                     NewsPodcast, RadioPodcast, ProjectPodcast,
                     Playlist)


for model in (NewsShow, RadioShow, ProjectShow,
              NewsPodcast, RadioPodcast, ProjectPodcast,
              Playlist):
    admin.site.register(model)
