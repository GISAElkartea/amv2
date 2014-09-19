from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^', include('radio.shows.urls')),
    url(r'^playlists', include('radio.playlists.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
