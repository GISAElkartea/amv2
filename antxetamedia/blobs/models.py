# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models, transaction
from django.core.exceptions import ValidationError
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

    def __str__(self):
        return self.name


class BlobQuerySet(models.QuerySet):
    def with_content(self):
        query = ((models.Q(remote__isnull=False) & ~models.Q(remote='')) |
                 (models.Q(local__isnull=False) & ~models.Q(local='')))
        return self.filter(query)


@python_2_unicode_compatible
class Blob(models.Model):
    objects = BlobQuerySet.as_manager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('Audio blob')
        verbose_name_plural = _('Audio blobs')

    content_type = models.ForeignKey('contenttypes.contenttype')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    position = models.PositiveIntegerField(_('Position'), default=0)

    local = models.FileField(_('Local file'), upload_to='blobs', null=True, blank=True, max_length=512,
                             help_text=_("If set, the file will be uploaded to the remote storage and the link will "
                                         "be set at the remote field."))
    remote = models.CharField(_('Remote file'), max_length=512, null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name=_('Account'))

    def __str__(self):
        return '{self.content_object} - #{self.position}'.format(self=self)

    @property
    def is_uploaded(self):
        return bool(not self.local and self.remote)

    @property
    def link(self):
        if self.local:
            return self.local.url
        if self.remote:
            return self.remote
        return ''

    def clean(self):
        if not self.local and not self.remote:
            raise ValidationError(_("Blobs should have either a local or a remote file."))


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
