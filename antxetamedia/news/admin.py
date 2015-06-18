from django.contrib import admin

from antxetamedia.blobs.admin import BlobInline
from .models import NewsCategory, NewsShow, NewsPodcast


class NewsPodcastAdmin(admin.ModelAdmin):
    inlines = [BlobInline]


admin.site.register(NewsCategory)
admin.site.register(NewsShow)
admin.site.register(NewsPodcast, NewsPodcastAdmin)
