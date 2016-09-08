from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from grappelli.forms import GrappelliSortableHiddenMixin

from .models import Account, Blob, BlobUpload
from .tasks import queue_blob_upload
from .forms import BlobForm
from .fields import UploadWidget


class BlobInline(GrappelliSortableHiddenMixin, GenericTabularInline):
    form = BlobForm
    fields = ['position', 'account', 'created', 'local', 'remote']
    model = Blob
    ordering = ['position']
    sortable_field_name = 'position'
    readonly_fields = ['created', 'remote']
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1


class IsUploadedFilter(admin.SimpleListFilter):
    title = _('Is uploaded')
    parameter_name = 'is_uploaded'

    def lookups(self, request, model_admin):
        return (('1', _('Yes')),
                ('0', _('No')))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(local__isnull=True, remote__isnull=False)
        if self.value() == '0':
            return queryset.filter(local__isnull=False, remote__isnull=True)
        return queryset


class BlobAdmin(admin.ModelAdmin):
    form = BlobForm
    list_display = ['__str__', 'get_content_object', 'get_last_upload', 'created', 'account', 'is_uploaded']
    list_filter = [IsUploadedFilter, 'created', 'account']
    readonly_fields = ['get_content_object', 'get_last_upload', 'remote', 'created']
    fields = ['get_content_object', 'get_last_upload', 'account', 'created', 'local', 'remote']
    actions = ['retry_upload']
    formfield_overrides = {models.FileField: {'widget': UploadWidget}}

    def get_content_object(self, instance):
        obj = instance.content_object
        if obj is not None:
            change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=obj._meta)
            change_url = reverse(change_name, args=(obj.pk,))
            return '<a href="{}">{}</a>'.format(change_url, obj)
    get_content_object.short_description = _('Podcast')
    get_content_object.allow_tags = True

    def get_last_upload(self, instance):
        upload = BlobUpload.objects.filter(blob=instance).last()
        if upload is not None:
            change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=upload._meta)
            change_url = reverse(change_name, args=(upload.pk,))
            return '<a href="{}">{}</a>'.format(change_url, upload)
    get_last_upload.short_description = _('Last upload')
    get_last_upload.allow_tags = True

    def is_uploaded(self, instance):
        return instance.is_uploaded
    is_uploaded.short_description = _('Has been uploaded')
    is_uploaded.boolean = True

    def retry_upload(self, request, queryset):
        for blob in queryset.iterator():
            queue_blob_upload(Blob, blob)
    retry_upload.short_description = _('Retry upload')

    def has_add_permission(self, request):
        return False


class BlobUploadAdmin(admin.ModelAdmin):
    list_display = ['started', 'ended', 'get_blob', 'get_state_boolean', 'get_state_display', 'get_traceback']
    list_filter = ['state']
    fields = ['get_blob', 'state', 'started', 'ended', 'get_link', 'traceback']
    readonly_fields = ['get_blob', 'state', 'started', 'ended', 'get_link', 'traceback']

    def get_blob(self, instance):
        change_name = 'admin:{meta.app_label}_{meta.model_name}_change'.format(meta=instance.blob._meta)
        change_url = reverse(change_name, args=(instance.blob.pk,))
        return '<a href="{}">{}</a>'.format(change_url, instance.blob)
    get_blob.short_description = _('Blob')
    get_blob.allow_tags = True

    def get_link(self, instance):
        link = instance.blob.remote
        if link:
            return '<a href="{link}">{link}</a>'.format(link=link)
        return ''
    get_link.short_description = _('Link')
    get_link.allow_tags = True

    def get_state_boolean(self, instance):
        return instance.has_succeeded()
    get_state_boolean.short_description = _('Has succeeded')
    get_state_boolean.boolean = True

    def get_state_display(self, instance):
        return instance.get_state_display()
    get_state_display.short_description = _('State')

    def get_traceback(self, instance):
        return instance.traceback.replace('\n', '<br/>')
    get_traceback.short_description = _('Traceback')
    get_traceback.allow_tags = True
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
admin.site.register(Blob, BlobAdmin)
admin.site.register(BlobUpload, BlobUploadAdmin)
