from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.utils.timezone import now

from autoslug import AutoSlugField
from antxetamedia.blobs.fields import RelatedBlobField


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


@python_2_unicode_compatible
class AbstractShow(models.Model):
    class Meta:
        abstract = True
        unique_together = [('category', 'slug')]

    name = models.CharField(_('Name'), max_length=256)
    slug = AutoSlugField(_('Slug'), populate_from='name', editable=True, unique_with='category')
    description = models.TextField(_('Description'), blank=True)  # TODO: Markup, CKEditor?
    featured = models.BooleanField(_('Featured'), default=False)
    image = models.ImageField(_('Image'), upload_to='shows', blank=True)  # TODO: something fancier?

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractPodcast(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(_('Title'), max_length=512)
    slug = AutoSlugField(_('Slug'), populate_from='title', editable=False, unique_with='show')
    description = models.TextField(_('Description'), blank=True)  # TODO: Markup, CKEditor?
    pub_date = models.DateTimeField(_('Publication date'), default=now)
    image = models.ImageField(_('Image'), upload_to='shows', blank=True)  # TODO: something fancier?
    blob = RelatedBlobField()

    def __str__(self):
        return self.title
