from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import (NewsShow, RadioShow, ProjectShow,
                     NewsPodcast, RadioPodcast, ProjectPodcast,
                     NewsCategory, RadioCategory, ProjectCategory,
                     Playlist)


class ShowAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


for model in NewsShow, RadioShow, ProjectShow:
    admin.site.register(model, ShowAdmin)


class PodcastAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


for model in NewsPodcast, RadioPodcast, ProjectPodcast:
    admin.site.register(model, PodcastAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


for model in NewsCategory, RadioCategory, ProjectCategory:
    admin.site.register(model, CategoryAdmin)


admin.site.register(Playlist)
