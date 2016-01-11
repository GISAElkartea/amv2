import json

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .fields import UniqueTrueBooleanField
from antxetamedia.shows.models import (AbstractCategory, AbstractShow, AbstractPodcast,
                                       CategoryManager, ShowManager, PodcastQuerySet)


NEWSCATEGORIES_COOKIE = getattr(settings, 'NEWSCATEGORIES_COOKIE', 'newscategories')


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


class NewsPodcastQuerySet(PodcastQuerySet):
    def favourites(self, request):
        qs = self
        newscategories = request.COOKIES.get(NEWSCATEGORIES_COOKIE)
        if newscategories:
            newscategories = json.loads(newscategories)
            qs = qs.filter(categories__pk__in=newscategories)
        return qs


class NewsPodcast(AbstractPodcast):
    objects = NewsPodcastQuerySet.as_manager()

    class Meta:
        ordering = ['-featured', '-pub_date']
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('Show'))
    categories = models.ManyToManyField(NewsCategory, verbose_name=_('Categories'))
    featured = UniqueTrueBooleanField(_('Featured'), default=False)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
