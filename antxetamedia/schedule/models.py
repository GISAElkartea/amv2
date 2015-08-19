from django.db import models
from django.utils.dates import WEEKDAYS
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Broadcast(models.Model):
    class Meta:
        ordering = ['weekday']
        verbose_name = _('Broadcast')
        verbose_name_plural = _('Broadcasts')

    weekday = models.PositiveSmallIntegerField(_('Weekday'), choices=WEEKDAYS.items())
    beginning = models.TimeField(_('Beginning'))

    name = models.CharField(_('Name'), max_length=64)
    description = models.CharField(_('Description'), max_length=512, blank=True)
    link = models.CharField(_('Link'), max_length=256, blank=True,
                            help_text=_('If the link is local, do not prepend the schema and the domain: '
                                        'use /some/path instead of https://domain.tld/some/path'))

    def __str__(self):
        return self.name
