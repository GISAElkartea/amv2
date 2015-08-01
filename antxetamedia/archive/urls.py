from django.conf.urls import include, url

from . import views


archive = [
    url(r'^$', views.SearchView.as_view(), name='search'),
    url(r'^news/$', views.NewsPodcastSearchView.as_view(), name='news'),
    url(r'^radio/$', views.RadioPodcastSearchView.as_view(), name='radio'),
    url(r'^projects/$', views.ProjectShowSearchView.as_view(), name='projects'),
    url(r'^events/$', views.EventSearchView.as_view(), name='events'),
]

urlpatterns = [url(r'^', include(archive, namespace='archive'))]
