from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from antxetamedia.blobs.admin import BlobInline
from .models import RadioCategory, RadioProducer, RadioShow, RadioPodcast


class RadioCategoryAdmin(admin.ModelAdmin):
    fields = [('name', 'slug')]
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


class RadioProducerAdmin(admin.ModelAdmin):
    fields = [('name', 'slug')]
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


class RadioShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'producer', 'category', 'featured']
    list_display_links = ['name', 'producer', 'category']
    list_editable = ['featured']
    list_filter = ['producer', 'category', 'featured']
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {
            'fields': [('name', 'slug'), 'featured', 'category', 'producer']}),
        (_('Details'), {
            'fields': ['image', 'description']}),
    ]


class RadioPodcastAdmin(admin.ModelAdmin):
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

    def get_changeform_initial_data(self, request):
        return {'title': _('Complete program')}


admin.site.register(RadioCategory, RadioCategoryAdmin)
admin.site.register(RadioProducer, RadioProducerAdmin)
admin.site.register(RadioShow, RadioShowAdmin)
admin.site.register(RadioPodcast, RadioPodcastAdmin)
