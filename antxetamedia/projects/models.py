from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from antxetamedia.shows.models import (AbstractProducer, AbstractShow, AbstractPodcast,
                                       ProducerManager, ShowQuerySet, PodcastManager)


class ProjectProducer(AbstractProducer):
    objects = ProducerManager()

    class Meta:
        verbose_name = _('Project producer')
        verbose_name_plural = _('Project producers')


class ProjectShowManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ShowQuerySet(self.model, using=self._db)


class ProjectShow(AbstractShow):
    objects = ProjectShowManager()

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    producer = models.ForeignKey(ProjectProducer, verbose_name=_('Producer'))
    creation_date = models.DateField(_('Creation date'), default=now,
                                     help_text=_('Only the year is taken into account'))

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})


class ProjectPodcast(AbstractPodcast):
    objects = PodcastManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('Project podcast')
        verbose_name_plural = _('Project podcasts')

    show = models.ForeignKey(ProjectShow, verbose_name=_('Show'))

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
