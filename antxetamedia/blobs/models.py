# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models, transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


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


@python_2_unicode_compatible
class Blob(models.Model):
    class Meta:
        unique_together = [('content_type', 'object_id', 'counter')]
        verbose_name = _('Audio blob')
        verbose_name_plural = _('Audio blobs')

    content_type = models.ForeignKey('contenttypes.contenttype')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    counter = models.PositiveIntegerField(default=0, editable=False)

    local = models.FileField(_('Local file'), upload_to='podcasts', null=True, blank=True,
                             help_text=_("If set, the file will be uploaded to the remote storage and the link will "
                                         "be set at the remote field."))
    remote = models.CharField(_('Remote file'), max_length=512, null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name=_('Account'))
    license = models.ForeignKey(License, verbose_name=_('License'))

    def __str__(self):
        return '{self.content_object} - #{self.counter}'.format(self=self)

    def save(self, *args, **kwargs):
        if not self.pk:
            qs = Blob.objects.filter(content_type=self.content_type, object_id=self.object_id)
            latest = qs.aggregate(latest=models.Max('counter'))['latest'] or 0
            self.counter = latest + 1
        return super(Blob, self).save(*args, **kwargs)

    @property
    def blob(self):
        if self.local:
            return self.local.url
        return self.remote


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
    started = models.DateTimeField(_('Start time'), null=True, blank=True)
    ended = models.DateTimeField(_('End time'), null=True, blank=True)
    traceback = models.TextField(_('Traceback'), blank=True)

    def __str__(self):
        return _('{blob} upload').format(blob=self.blob)

    def has_succeeded(self):
        if self.state in (self.SUCCEEDED, self.FAILED):
            return self.state == self.SUCCEEDED
        return None

    def is_uploading(self):
        self.started = timezone.now()
        self.state = self.UPLOADING
        self.save()

    def is_successful(self, remote):
        with transaction.atomic():
            self.ended = timezone.now()
            self.state = self.SUCCEEDED
            self.save()
            self.blob.remote = remote
            self.blob.local.delete()
            self.blob.save()

    def is_unsuccessful(self, traceback=None):
        self.ended = timezone.now()
        self.state = self.FAILED
        self.traceback = traceback
        self.save()
