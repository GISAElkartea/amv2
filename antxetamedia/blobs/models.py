from django.db import models, transaction
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


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
        unique_together = [('content_type', 'object_id', 'counter')]
        verbose_name = _('Blob')
        verbose_name_plural = _('Blobs')

    content_type = models.ForeignKey('contenttypes.contenttype')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    counter = models.PositiveIntegerField(default=0, editable=False)

    local = models.FileField(_('Local file'), upload_to='podcasts', null=True, blank=True,
                             help_text=_("If set, the file will be uploaded to the remote storage and the link will "
                                         "be set at the remote field."))
    remote = models.URLField(_('Remote file'), null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name=_('Account'))
    license = models.ForeignKey(License, verbose_name=_('License'))

    def __str__(self):
        return '{self.content_object} - #{self.counter}'.format(self=self)

    def save(self, *args, **kwargs):
        if not self.pk:
            qs = Blob.objects.filter(content_type=self.content_type, object_id=self.object_id)
            latest = qs.aggregate(latest=models.Max('counter'))['latest']
            self.counter = latest + 1
        return super(Blob, self).save(*args, **kwargs)

    @property
    def blob(self):
        return self.local or self.remote


@python_2_unicode_compatible
class BlobUpload(models.Model):
    PENDING = 0
    UPLOADING = 1
    SUCCEEDED = 2
    FAILED = 3
    STATES = [
        (PENDING, _('Pending')),
        (UPLOADING, _('Uploading')),
        (SUCCEEDED, _('Succeeded')),
        (FAILED, _('Failed')),
    ]

    class Meta:
        verbose_name = _('Blob upload')
        verbose_name_plural = _('Blob uploads')

    blob = models.ForeignKey(Blob, verbose_name=_('Blob'))
    state = models.PositiveSmallIntegerField(_('State'), choices=STATES, default=PENDING)
    result = models.TextField(_('Result'), blank=True)  # JSONField?

    def __str__(self):
        return _('{blob} upload').format(blob=self.blob)

    def upload(self):
        self.state = self.UPLOADING
        self.save()
        try:
            # Do whatever needs to be done
            remote = None
        except:  # Some uploading exception
            self.state = self.FAILED
            self.save()
        else:
            with transaction.atomic():
                self.state = self.SUCCEEDED
                self.save()
                self.blob.remote = remote
                self.blob.save()
