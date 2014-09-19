from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedRouterMixin

from .views import UserPlaylists, PlaylistElements


class Router(ExtendedRouterMixin, DefaultRouter):
    pass


router = Router()
playlist_router = router.register(r'playlists', UserPlaylists,
                                  base_name='playlist')
playlist_router.register(r'elements', PlaylistElements,
                         base_name='playlist-element',
                         parents_query_lookups=['playlist'])

urlpatterns = router.urls
