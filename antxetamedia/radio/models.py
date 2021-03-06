import json

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from antxetamedia.shows.models import (AbstractCategory, AbstractProducer, AbstractShow, AbstractPodcast,
                                       CategoryManager, ProducerManager, ShowManager, PodcastQuerySet)


RADIOSHOWS_COOKIE = getattr(settings, 'RADIOSHOWS_COOKIE', 'radioshows')


class RadioCategory(AbstractCategory):
    objects = CategoryManager()

    class Meta:
        verbose_name = _('Radio category')
        verbose_name_plural = _('Radio categories')

    def get_absolute_url(self):
        return reverse('radio:list') + '?category=' + self.slug


class RadioProducer(AbstractProducer):
    objects = ProducerManager()

    class Meta:
        verbose_name = _('Radio producer')
        verbose_name_plural = _('Radio producers')

    def get_absolute_url(self):
        return reverse('radio:list') + '?producer=' + self.slug


class RadioShowQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)


class RadioShow(AbstractShow):
    objects = ShowManager.from_queryset(RadioShowQuerySet)()

    class Meta:
        verbose_name = _('Radio show')
        verbose_name_plural = _('Radio shows')

    category = models.ForeignKey(RadioCategory, null=True, blank=True, verbose_name=_('Category'))
    producer = models.ForeignKey(RadioProducer, verbose_name=_('Producer'))
    featured = models.BooleanField(_('Featured'), default=False)

    def get_absolute_url(self):
        return reverse('radio:podcasts', kwargs={'slug': self.slug})


class RadioPodcastQuerySet(PodcastQuerySet):
    def favourites(self, request):
        qs = self
        radioshows = request.COOKIES.get(RADIOSHOWS_COOKIE)
        if radioshows:
            radioshows = json.loads(radioshows)
            qs = qs.filter(show__pk__in=radioshows)
        return qs


class RadioPodcast(AbstractPodcast):
    objects = RadioPodcastQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('Radio podcast')
        verbose_name_plural = _('Radio podcasts')

    show = models.ForeignKey(RadioShow, verbose_name=_('Show'))

    def get_absolute_url(self):
        return reverse('radio:podcasts', kwargs={'slug': self.show.slug})
