from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Broadcast


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_link', 'weekday', 'beginning', 'ending']
    list_filter = ['weekday', 'beginning', 'ending']
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {
            'fields': [('name', 'link'), 'description']}),
        (_('When'), {
            'fields': [('weekday', 'beginning', 'ending')]}),
    ]

    def get_link(self, obj):
        if obj.link:
            return '<a href="{obj.link}">{obj.link}</a>'.format(obj=obj)
        return ''
    get_link.allow_tags = True
    get_link.short_description = _('Link')


admin.site.register(Broadcast, BroadcastAdmin)
