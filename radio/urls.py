from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import playlists


router = routers.DefaultRouter()

#router.register(r'news/categories', views.NewsCategoryViewSet)
#router.register(r'news/shows', views.NewsShowViewSet)
#router.register(r'news/podcasts', views.NewsPodcastViewSet)

#router.register(r'radio/categories', views.RadioCategoryViewSet)
#router.register(r'radio/shows', views.RadioShowViewSet)
#router.register(r'radio/podcasts', views.RadioPodcastViewSet)

#router.register(r'projects/categories', views.ProjectCategoryViewSet)
#router.register(r'projects/shows', views.ProjectShowViewSet)
#router.register(r'projects/podcasts', views.ProjectPodcastViewSet)

router.register(r'playlists/user', playlists.UserPlaylists,
                base_name='playlist')
router.register(r'playlists/positions', playlists.PlaylistPositions,
                base_name='playlist-position')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
