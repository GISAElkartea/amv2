from django.contrib import admin

from antxetamedia.blobs.admin import BlobInline
from .models import NewsCategory, NewsProducer, NewsShow, NewsPodcast


class NewsPodcastAdmin(admin.ModelAdmin):
    inlines = [BlobInline]


admin.site.register(NewsCategory)
admin.site.register(NewsProducer)
admin.site.register(NewsShow)
admin.site.register(NewsPodcast, NewsPodcastAdmin)
