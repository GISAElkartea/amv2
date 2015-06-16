from django.contrib import admin

from antxetamedia.blobs.admin import BlobInline
from .models import ProjectProducer, ProjectShow, ProjectPodcast


class ProjectPodcastAdmin(admin.ModelAdmin):
    inlines = [BlobInline]


admin.site.register(ProjectProducer)
admin.site.register(ProjectShow)
admin.site.register(ProjectPodcast, ProjectPodcastAdmin)
