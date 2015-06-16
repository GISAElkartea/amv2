from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

from .models import Playlist, PlaylistElement


class PlaylistElementAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaylistElement


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistElementAdmin]


admin.site.register(Playlist, PlaylistAdmin)
