from django.conf.urls import include, url

from .views import EventList, EventDetail


expressions = {
    'event': r'(?P<slug>[\w-]+)',
}

events = [
    url(r'^$', EventList.as_view(), name='list'),
    url(r'^{event}/$'.format(**expressions), EventDetail.as_view(), name='detail'),
]

urlpatterns = [url(r'^', include(events, namespace='events'))]
