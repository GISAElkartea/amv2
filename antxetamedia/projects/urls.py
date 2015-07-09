from django.conf.urls import include, url

from .views import ProjectProducerList, ProjectShowDetail


expressions = {
    'projectshow': r'(?P<slug>[\w-]+)',
}

radio = [
    url(r'^$', ProjectProducerList.as_view(), name='list'),
    url(r'^{projectshow}/$'.format(**expressions), ProjectShowDetail.as_view(), name='detail'),
]

urlpatterns = [url(r'^', include(radio, namespace='projects'))]
