from django.conf.urls import include, url

from . import views


archive = [
    url(r'^$', views.SearchView.as_view(), name='search'),
]

urlpatterns = [url(r'^', include(archive, namespace='archive'))]
