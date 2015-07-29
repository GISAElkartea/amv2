from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def build_absolute_uri(context, url):
    if url:
        return context['request'].build_absolute_uri(url)
