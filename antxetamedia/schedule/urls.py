from django.conf.urls import include, url

from .views import BroadcastList


schedule = [
    url(r'^$', BroadcastList.as_view(), name='list'),
]

urlpatterns = [url(r'^', include(schedule, namespace='schedule'))]
