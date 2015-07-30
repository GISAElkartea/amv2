from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.admin import AdminImageMixin

from antxetamedia.blobs.admin import BlobInline
from .models import ProjectProducer, ProjectShow, ProjectPodcast


class ProjectProducerAdmin(admin.ModelAdmin):
    fields = [('name', 'slug')]
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


class ProjectShowAdmin(AdminImageMixin, admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ['name', 'slug', 'producer', 'creation_date']
    list_display_links = ['name', 'producer']
    list_filter = ['producer', 'creation_date']
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {
            'fields': [('name', 'slug'), 'creation_date', 'producer']}),
        (_('Details'), {
            'fields': ['image', 'description']}),
    ]


class ProjectPodcastAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [BlobInline]
    date_hierarchy = 'pub_date'
    list_display = ['title', 'show', 'pub_date']
    list_display_links = ['title', 'show']
    list_filter = ['show', 'pub_date']
    search_fields = ['title', 'description']
    fieldsets = [
        (None, {
            'fields': ['title', 'show', 'pub_date']}),
        (_('Details'), {
            'fields': ['image', 'description']}),
    ]


admin.site.register(ProjectProducer, ProjectProducerAdmin)
admin.site.register(ProjectShow, ProjectShowAdmin)
admin.site.register(ProjectPodcast, ProjectPodcastAdmin)
