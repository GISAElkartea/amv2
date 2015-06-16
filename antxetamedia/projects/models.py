from django.db import models
from django.utils.translation import ugettext as _

from antxetamedia.shows.models import AbstractProducer, AbstractShow, AbstractPodcast


class ProjectProducer(AbstractProducer):
    class Meta:
        verbose_name = _('Project producer')
        verbose_name_plural = _('Project producers')


class ProjectShow(AbstractShow):
    class Meta:
        verbose_name = _('Project show')
        verbose_name_plural = _('Project shows')

    producer = models.ForeignKey(ProjectProducer, verbose_name=_('Producer'))


class ProjectPodcast(AbstractPodcast):
    class Meta:
        verbose_name = _('Project podcast')
        verbose_name_plural = _('Project podcasts')

    show = models.ForeignKey(ProjectShow, verbose_name=_('Show'))
