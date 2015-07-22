from django.contrib import admin

from .models import Flatpage


class FlatpageAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'on_menu']
    list_editable = ['on_menu']
    list_filter = ['on_menu']
    search_fields = ['name', 'content']
    fields = [('name', 'slug'), 'on_menu', 'content']


admin.site.register(Flatpage, FlatpageAdmin)
