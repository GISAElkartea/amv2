from django.contrib import admin
from django.utils.text import ugettext_lazy as _

from antxetamedia.blobs.admin import BlobInline
from .models import NewsCategory, NewsShow, NewsPodcast


class NewsCategoryAdmin(admin.ModelAdmin):
    fields = [('name', 'slug')]
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


class NewsShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {
            'fields': ['name', 'slug']}),
        (_('Details'), {
            'fields': ['image', 'description']}),
    ]


class NewsPodcastAdmin(admin.ModelAdmin):
    inlines = [BlobInline]
    date_hierarchy = 'pub_date'
    list_display = ['title', 'show', 'pub_date']
    list_display_links = ['title', 'show']
    list_filter = ['show', 'categories', 'pub_date']
    search_fields = ['title', 'description']
    fieldsets = [
        (None, {
            'fields': ['title', 'show', 'categories', 'pub_date']}),
        (_('Details'), {
            'fields': ['image', 'description']}),
    ]


admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(NewsShow, NewsShowAdmin)
admin.site.register(NewsPodcast, NewsPodcastAdmin)
