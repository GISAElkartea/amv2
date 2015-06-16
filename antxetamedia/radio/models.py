from django.db import models
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import AbstractCategory, AbstractProducer, AbstractShow, AbstractPodcast


class RadioCategory(AbstractCategory):
    class Meta:
        verbose_name = _('Radio category')
        verbose_name_plural = _('Radio categories')


class RadioProducer(AbstractProducer):
    class Meta:
        verbose_name = _('Radio producer')
        verbose_name_plural = _('Radio producers')


class RadioShow(AbstractShow):
    class Meta:
        verbose_name = _('Radio show')
        verbose_name_plural = _('Radio shows')

    category = models.ForeignKey(RadioCategory, verbose_name=_('Category'))
    producer = models.ForeignKey(RadioProducer, verbose_name=_('Producer'))


class RadioPodcast(AbstractPodcast):
    class Meta:
        verbose_name = _('Radio podcast')
        verbose_name_plural = _('Radio podcasts')

    show = models.ForeignKey(RadioShow, verbose_name=_('Show'))
