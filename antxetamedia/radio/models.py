from django.db import models
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import (AbstractCategory, AbstractProducer, AbstractShow, AbstractPodcast,
                                       CategoryManager, ProducerManager, ShowManager, PodcastManager)


class RadioCategory(AbstractCategory):
    objects = CategoryManager()

    class Meta:
        verbose_name = _('Radio category')
        verbose_name_plural = _('Radio categories')


class RadioProducer(AbstractProducer):
    objects = ProducerManager()

    class Meta:
        verbose_name = _('Radio producer')
        verbose_name_plural = _('Radio producers')


class RadioShow(AbstractShow):
    objects = ShowManager()

    class Meta:
        verbose_name = _('Radio show')
        verbose_name_plural = _('Radio shows')

    category = models.ForeignKey(RadioCategory, verbose_name=_('Category'))
    producer = models.ForeignKey(RadioProducer, verbose_name=_('Producer'))


class RadioPodcast(AbstractPodcast):
    objects = PodcastManager()

    class Meta:
        verbose_name = _('Radio podcast')
        verbose_name_plural = _('Radio podcasts')

    show = models.ForeignKey(RadioShow, verbose_name=_('Show'))
