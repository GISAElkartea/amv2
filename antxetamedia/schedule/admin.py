from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Label, Broadcast


class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'colour']
    fields = [('name', 'colour')]
    search_fields = ['name']


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_link', 'weekday', 'beginning', 'ending', 'foreground', 'background']
    list_display_links = ['name', 'foreground', 'background']
    list_filter = ['weekday', 'beginning', 'ending', 'foreground', 'background']
    search_fields = ['name']
    fieldsets = [
        (None, {
            'fields': [('name', 'link'), ('foreground', 'background')]}),
        (_('When'), {
            'fields': [('weekday', 'beginning', 'ending')]}),
    ]

    def get_link(self, obj):
        if obj.link:
            return '<a href="{obj.link}">{obj.link}</a>'.format(obj=obj)
        return ''
    get_link.allow_tags = True
    get_link.short_description = _('Link')


admin.site.register(Label, LabelAdmin)
admin.site.register(Broadcast, BroadcastAdmin)
