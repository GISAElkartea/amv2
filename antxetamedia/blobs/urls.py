from django.conf.urls import include, url

from .views import PodcastBlobList


expressions = {
    'app_label': r'(?P<app_label>[\w-]+)',
    'model': r'(?P<model>[\w-]+)',
    'id': r'(?P<id>\d+)',
}

news = [
    url(r'^{app_label}/{model}/{id}/$'.format(**expressions), PodcastBlobList.as_view(), name='podcast'),
]

urlpatterns = [url(r'^', include(news, namespace='blobs'))]
