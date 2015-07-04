from django.contrib import admin

from .models import Flatpage


class FlatpageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Flatpage, FlatpageAdmin)
