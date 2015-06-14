from django.db import models
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    name = models.CharField(_('Name'), max_length=64)
    username = models.CharField(_('Username'), max_length=256)
    password = models.CharField(_('Password'), max_length=256)
    # metadata goes here

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class License(models.Model):
    class Meta:
        verbose_name = _('License')
        verbose_name_plural = _('Licenses')

    name = models.CharField(_('Name'), max_length=64)
    link = models.URLField(_('Link'))

    def __str__(self):
        return self.name


class UniqueGenericForeignKey(GenericForeignKey):
    related_accessor_class = SingleRelatedObjectDescriptor


@python_2_unicode_compatible
class Blob(models.Model):
    class Meta:
        # Effectively a OneToOne relationship
        unique_together = [('content_type', 'object_id')]
        verbose_name = _('Blob')
        verbose_name_plural = _('Blobs')

    content_type = models.ForeignKey('contenttypes.contenttype')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    local = models.FileField(_('Local file'), upload_to='podcasts', null=True, blank=True,
                             help_text=_("If set, the file will be uploaded to the remote storage and the link will "
                                         "be set at the remote field."))
    remote = models.URLField(_('Remote file'), null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name=_('Account'))
    license = models.ForeignKey(License, verbose_name=_('License'))

    def __str__(self):
        return _('Blob for {}').format(self.content_object)
