from django.db import models
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import AbstractCategory, AbstractProducer, AbstractShow, AbstractPodcast


class NewsCategory(AbstractCategory):
    class Meta:
        verbose_name = _('News category')
        verbose_name_plural = _('News categories')


class NewsProducer(AbstractProducer):
    class Meta:
        verbose_name = _('News producer')
        verbose_name_plural = _('News producers')


class NewsShow(AbstractShow):
    class Meta:
        verbose_name = _('News show')
        verbose_name_plural = _('News shows')

    category = models.ForeignKey(NewsCategory, verbose_name=_('Category'))
    producer = models.ForeignKey(NewsProducer, verbose_name=_('Producer'))


class NewsPodcast(AbstractPodcast):
    class Meta:
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('Show'))