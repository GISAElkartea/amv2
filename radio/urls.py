from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework_extensions.routers import ExtendedRouterMixin

from .views import playlists


class Router(ExtendedRouterMixin, DefaultRouter):
    pass


router = Router()
playlist_router = router.register(r'playlists', playlists.UserPlaylists,
                                  base_name='playlist')
playlist_router.register(r'podcasts', playlists.PlaylistElements,
                         base_name='playlist-element',
                         parents_query_lookups=['playlist'])

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
