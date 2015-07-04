from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible

from ckeditor.fields import RichTextField


class FlatpageQuerySet(models.QuerySet):
    def on_menu(self):
        return self.filter(on_menu=True)


@python_2_unicode_compatible
class Flatpage(models.Model):
    objects = FlatpageQuerySet.as_manager()

    class Meta:
        verbose_name = _('Flatpage')
        verbose_name_plural = _('Flatpages')

    on_menu = models.BooleanField(_('One menu'), default=False)
    name = models.CharField(_('Name'), max_length=128)
    path = models.SlugField(_('Path'), max_length=128, unique=True)
    content = RichTextField(_('Content'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('flatpages:detail', kwargs={'slug': self.path})
