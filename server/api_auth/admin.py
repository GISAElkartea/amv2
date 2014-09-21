from django.contrib import admin

from custom_user.admin import EmailUserAdmin

from .models import APIUser


class APIUserAdmin(EmailUserAdmin):
    pass


admin.site.register(APIUser, APIUserAdmin)
