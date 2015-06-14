from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Account, License, Blob


class BlobInline(GenericTabularInline):
    model = Blob
    fields = ['account', 'license', 'local', 'remote']
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1
    max_num = 1


class BlobAdmin(admin.ModelAdmin):
    readonly_fields = ['content_object']
    fields = ['content_object', 'account', 'license', 'local', 'remote']

    def content_object(self, instance):
        change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=instance.content_object._meta)
        change_url = reverse(change_name, args=(instance.content_object.pk,))
        return '<a href="{}">{}</a>'.format(change_url, instance.content_object)
    content_object.short_description = _('Podcast')
    content_object.allow_tags = True


admin.site.register(Account)
admin.site.register(License)
admin.site.register(Blob, BlobAdmin)
