from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.utils.timezone import now

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

from antxetamedia.blobs.models import Blob


@python_2_unicode_compatible
class AbstractCategory(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractProducer(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name


class ShowQuerySet(models.QuerySet):
    def published(self):
        return self.filter(pub_date__lte=now())

    def unpublished(self):
        return self.filter(pub_date__gt=now())


@python_2_unicode_compatible
class AbstractShow(models.Model):
    objects = ShowQuerySet.as_manager()

    class Meta:
        abstract = True
        unique_together = [('category', 'slug')]

    name = models.CharField(_('Name'), max_length=256)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique_with='category')
    description = RichTextField(_('Description'), blank=True)
    featured = models.BooleanField(_('Featured'), default=False)
    image = models.ImageField(_('Image'), upload_to='shows', blank=True)  # TODO: something fancier?

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractPodcast(models.Model):
    class Meta:
        ordering = ['pub_date']
        abstract = True

    title = models.CharField(_('Title'), max_length=512)
    slug = AutoSlugField(_('Slug'), populate_from='title', editable=False, unique_with='show')
    description = RichTextField(_('Description'), blank=True)
    pub_date = models.DateTimeField(_('Publication date'), default=now)
    image = models.ImageField(_('Image'), upload_to='shows', blank=True)  # TODO: something fancier?
    blob_set = GenericRelation(Blob, content_type_field='content_type', object_id_field='object_id')

    def __str__(self):
        return self.title
