from django.contrib import admin
from django.utils.text import ugettext_lazy as _

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location']
    list_filter = ['time', 'location']
    search_fields = ['title', 'description', 'location']
    fieldsets = [
        (_('Date & Time'), {
            'fields': ['time', 'recurrences']}),
        (_('Details'), {
            'fields': ['title', 'location', 'link', 'image', 'description']}),
    ]


admin.site.register(Event, EventAdmin)
