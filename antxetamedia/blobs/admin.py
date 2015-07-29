from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Account, License, Blob, BlobUpload


class BlobInline(GenericTabularInline):
    model = Blob
    fields = ['account', 'license', 'local', 'remote']
    readonly_fields = ['remote']
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1


class BlobAdmin(admin.ModelAdmin):
    list_display = ['blob', ]
    readonly_fields = ['get_content_object', 'remote']
    fields = ['get_content_object', 'account', 'license', 'local', 'remote']

    def get_content_object(self, instance):
        content_object = instance.content_object
        change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=content_object._meta)
        change_url = reverse(change_name, args=(content_object.pk,))
        return '<a href="{}">{}</a>'.format(change_url, content_object)
    get_content_object.short_description = _('Podcast')
    get_content_object.allow_tags = True


class BlobUploadAdmin(admin.ModelAdmin):
    list_display_links = ['get_content_object']
    list_display = ['blob', 'get_content_object', 'get_state_boolean', 'get_state_display', 'traceback']
    list_filter = ['state']

    def get_content_object(self, instance):
        content_object = instance.blob.content_object
        if content_object:
            change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=content_object._meta)
            change_url = reverse(change_name, args=(content_object.pk,))
            return '<a href="{}">{}</a>'.format(change_url, content_object)
    get_content_object.short_description = _('Podcast')
    get_content_object.allow_tags = True

    def get_state_boolean(self, instance):
        return instance.has_succeeded()
    get_state_boolean.short_description = _('Has succeeded')
    get_state_boolean.boolean = True

    def get_state_display(self, instance):
        return instance.get_state_display()
    get_state_display.short_description = _('State')

    # Remove the delete Admin Action for this Model
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Return nothing to make sure user can't update any data
        pass

admin.site.register(Account)
admin.site.register(License)
admin.site.register(Blob, BlobAdmin)
admin.site.register(BlobUpload, BlobUploadAdmin)
