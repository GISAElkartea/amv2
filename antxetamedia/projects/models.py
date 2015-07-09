from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import (AbstractProducer, AbstractShow, AbstractPodcast,
                                       ProducerManager, ShowManager, PodcastManager)


class ProjectProducer(AbstractProducer):
    objects = ProducerManager()

    class Meta:
        verbose_name = _('Project producer')
        verbose_name_plural = _('Project producers')


class ProjectShow(AbstractShow):
    objects = ShowManager()

    class Meta:
        verbose_name = _('Project show')
        verbose_name_plural = _('Project shows')

    producer = models.ForeignKey(ProjectProducer, verbose_name=_('Producer'))

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})


class ProjectPodcast(AbstractPodcast):
    objects = PodcastManager()

    class Meta:
        verbose_name = _('Project podcast')
        verbose_name_plural = _('Project podcasts')

    show = models.ForeignKey(ProjectShow, verbose_name=_('Show'))
