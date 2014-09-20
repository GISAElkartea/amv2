from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedRouterMixin

from .views import (NewsCategories, NewsShows, NewsPodcasts,
                    RadioCategories, RadioShows, RadioPodcasts,
                    ProjectCategories, ProjectShows, ProjectPodcasts)


class Router(ExtendedRouterMixin, DefaultRouter):
    pass


news_router = Router()
news_router.register(r'/categories', NewsCategories, base_name='news_category')
news_show_router = news_router.register(r'/shows', NewsShows,
                                        base_name='news_show')
news_show_router.register(r'/podcasts', NewsPodcasts, base_name='news_podcasts',
                          parents_query_lookups=['show'])

radio_router = Router()
radio_router.register(r'/categories', RadioCategories,
                      base_name='radio_category')
radio_show_router = radio_router.register(r'/shows', RadioShows,
                                          base_name='radio_show')
radio_show_router.register(r'/podcasts', RadioPodcasts,
                           base_name='radio_podcasts',
                           parents_query_lookups=['show'])

project_router = Router()
project_router.register(r'/categories', ProjectCategories,
                        base_name='project_category')
project_show_router = project_router.register(r'/shows', ProjectShows,
                                              base_name='project_show')
project_show_router.register(r'/podcasts', ProjectPodcasts,
                             base_name='project_podcasts',
                             parents_query_lookups=['show'])

urlpatterns = patterns(
    '',
    url(r'news', include(news_router.urls)),
    url(r'radio', include(radio_router.urls)),
    url(r'projects', include(project_router.urls)),
)
