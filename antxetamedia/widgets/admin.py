from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from .models import Widget


class WidgetAdmin(SortableAdminMixin, admin.ModelAdmin):
    fields = ['name', 'content']
    search_fields = ['content']


admin.site.register(Widget, WidgetAdmin)
