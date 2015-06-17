from django.db import models
from django.utils.dates import WEEKDAYS
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible

from colorful.fields import RGBColorField


@python_2_unicode_compatible
class Label(models.Model):
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    name = models.CharField(_('Name'), max_length=64)
    colour = RGBColorField(_('Colour'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Broadcast(models.Model):
    class Meta:
        verbose_name = _('Broadcast')
        verbose_name_plural = _('Broadcasts')

    weekday = models.PositiveSmallIntegerField(_('Weekday'), choices=WEEKDAYS.items())
    beginning = models.TimeField(_('Beginning'))
    ending = models.TimeField(_('Ending'))

    name = models.CharField(_('Name'), max_length=64)
    link = models.CharField(_('Link'), max_length=256, blank=True,
                            help_text=_('If the link is local, do not prepend the schema and the domain: '
                                        'use /some/path instead of https://domain.tld/some/path'))

    foreground = models.ForeignKey(Label, blank=True, null=True, related_name='+', verbose_name=_('Foreground label'))
    background = models.ForeignKey(Label, blank=True, null=True, related_name='+', verbose_name=_('Background label'))

    def __str__(self):
        return self.name
