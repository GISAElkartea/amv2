from django.contrib import admin

from antxetamedia.blobs.admin import BlobInline
from .models import RadioCategory, RadioProducer, RadioShow, RadioPodcast


class RadioPodcastAdmin(admin.ModelAdmin):
    inlines = [BlobInline]


admin.site.register(RadioCategory)
admin.site.register(RadioProducer)
admin.site.register(RadioShow)
admin.site.register(RadioPodcast, RadioPodcastAdmin)
