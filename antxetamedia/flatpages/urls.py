from django.conf.urls import include, url

from .views import FlatpageDetail


expressions = {
    'flatpage': r'(?P<slug>[\w-]+)',
}

news = [
    url(r'^{flatpage}/$'.format(**expressions), FlatpageDetail.as_view(), name='detail'),
]

urlpatterns = [url(r'^', include(news, namespace='flatpages'))]
