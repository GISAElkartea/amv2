from django.conf.urls import include, url

from .views import RadioShowList, RadioShowPodcastList


expressions = {
    'radioshow': r'(?P<slug>[\w-]+)',
}

radio = [
    url(r'^$', RadioShowList.as_view(), name='list'),
    url(r'^{radioshow}/$'.format(**expressions), RadioShowPodcastList.as_view(), name='podcasts'),
]

urlpatterns = [url(r'^', include(radio, namespace='radio'))]
