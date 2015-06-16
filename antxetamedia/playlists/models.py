from django.conf import settings
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Playlist(models.Model):
    class Meta:
        unique_together = ('user', 'title')
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    title = models.CharField(_('Title'), max_length=128)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class PlaylistElement(models.Model):
    class Meta:
        ordering = ['position']
        verbose_name = _('Playlist element')
        verbose_name_plural = _('Playlist element')

    playlist = models.ForeignKey(Playlist, verbose_name=_('Playlist'))
    blob = models.ForeignKey('blobs.Blob', verbose_name=_('Blob'))
    position = models.PositiveIntegerField(_('Position'), default=0)

    def __str__(self):
        return '#{self.position}: {self.blob.content_type}'.format(self=self)
