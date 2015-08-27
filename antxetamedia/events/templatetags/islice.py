import itertools

from django import template


register = template.Library()


@register.filter
def islice(iterator, stop):
    return itertools.islice(iterator, 0, int(stop))
