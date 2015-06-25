from django.db import models
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import AbstractCategory, AbstractShow, AbstractPodcast


class NewsCategory(AbstractCategory):
    class Meta:
        verbose_name = _('News category')
        verbose_name_plural = _('News categories')


class NewsShow(AbstractShow):
    class Meta:
        verbose_name = _('News show')
        verbose_name_plural = _('News shows')


class NewsPodcast(AbstractPodcast):
    class Meta:
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('Show'))
    categories = models.ManyToManyField(NewsCategory, blank=True, verbose_name=_('Categories'))
