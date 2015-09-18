from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Broadcast


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_link', 'weekday', 'beginning']
    list_filter = ['weekday', 'beginning']
    search_fields = ['name', 'classification']
    fieldsets = [
        (None, {
            'fields': [('name', 'link'), 'classification']}),
        (_('When'), {
            'fields': [('weekday', 'beginning')]}),
    ]

    def get_link(self, obj):
        if obj.link:
            return '<a href="{obj.link}">{obj.link}</a>'.format(obj=obj)
        return ''
    get_link.allow_tags = True
    get_link.short_description = _('Link')


admin.site.register(Broadcast, BroadcastAdmin)
