from django.db import models
from django.db.models.functions import Lower
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField

from antxetamedia.blobs.models import Blob


class CategoryManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(CategoryManager, self).get_queryset(*args, **kwargs).order_by(Lower('name'))


@python_2_unicode_compatible
class AbstractCategory(models.Model):
    objects = CategoryManager()

    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name


class ProducerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ProducerManager, self).get_queryset(*args, **kwargs).order_by(Lower('name'))


@python_2_unicode_compatible
class AbstractProducer(models.Model):
    objects = ProducerManager()

    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name


class ShowQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)


class ShowManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ShowQuerySet(self.model, using=self._db).order_by(Lower('name'))


@python_2_unicode_compatible
class AbstractShow(models.Model):
    objects = ShowManager()

    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=256)
    slug = AutoSlugField(_('Slug'), unique=True, populate_from='name', editable=True)
    description = RichTextField(_('Description'), blank=True)
    image = ImageField(_('Image'), upload_to='shows', blank=True)

    def __str__(self):
        return self.name


class PodcastQuerySet(models.QuerySet):
    def published(self):
        return self.filter(pub_date__lte=now())

    def unpublished(self):
        return self.filter(pub_date__gt=now())


PodcastManager = PodcastQuerySet.as_manager


@python_2_unicode_compatible
class AbstractPodcast(models.Model):
    objects = PodcastManager()

    class Meta:
        abstract = True

    title = models.CharField(_('Title'), max_length=512)
    slug = AutoSlugField(_('Slug'), populate_from='title', editable=False, unique_with='show')
    description = RichTextField(_('Description'), blank=True)
    pub_date = models.DateTimeField(_('Publication date'), default=now)
    image = ImageField(_('Image'), upload_to='shows', blank=True)
    blob_set = GenericRelation(Blob, content_type_field='content_type', object_id_field='object_id')

    def __str__(self):
        return self.title

    def get_blobs_url(self):
        return reverse('blobs:podcast', kwargs={
            'app_label': self._meta.app_label,
            'model': self._meta.model_name,
            'id': self.pk,
        })

    @property
    def metadata(self):
        return {
            'x-archive-meta-mediatype': 'audio',
            'x-archive-meta-collection': 'opensource_audio',
            'x-archive-meta-title': str(self),
            'x-archive-meta-creator': str(self.show),
            'x-archive-meta-description': self.description,
            'x-archive-meta-date': self.pub_date.strftime('%Y-%m-%d'),
            'x-archive-meta-language': 'eu',
        }
