from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import (AbstractCategory, AbstractShow, AbstractPodcast,
                                       CategoryManager, ShowManager, PodcastManager)


class NewsCategory(AbstractCategory):
    objects = CategoryManager()

    class Meta:
        verbose_name = _('News category')
        verbose_name_plural = _('News categories')

    def get_absolute_url(self):
        return reverse('news:category', kwargs={'slug': self.slug})


class NewsShow(AbstractShow):
    objects = ShowManager()

    class Meta:
        verbose_name = _('News show')
        verbose_name_plural = _('News shows')

    def get_absolute_url(self):
        return reverse('news:show', kwargs={'slug': self.slug})


class NewsPodcast(AbstractPodcast):
    objects = PodcastManager()

    class Meta:
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('Show'))
    categories = models.ManyToManyField(NewsCategory, blank=True, verbose_name=_('Categories'))

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
