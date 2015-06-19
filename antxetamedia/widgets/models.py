from django.db import models
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible

from ckeditor.fields import RichTextField


@python_2_unicode_compatible
class Widget(models.Model):
    class Meta:
        ordering = ['position']
        verbose_name = _('Widget')
        verbose_name_plural = _('Widgets')

    name = models.CharField(_('Name'), max_length=128)
    position = models.PositiveIntegerField(_('Position'), default=0)
    content = RichTextField(_('Content'))

    def __str__(self):
        return self.name
