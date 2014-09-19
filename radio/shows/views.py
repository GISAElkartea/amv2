from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from ..models import (NewsCategory, RadioCategory, ProjectCategory,
                      NewsShow, RadioShow, ProjectShow,
                      NewsPodcast, RadioPodcast, ProjectPodcast)

from .serializers import (NewsCategorySerializer,
                          RadioCategorySerializer,
                          ProjectCategorySerializer,
                          NewsShowSerializer,
                          RadioShowSerializer,
                          ProjectShowSerializer,
                          NewsPodcastSerializer,
                          RadioPodcastSerializer,
                          ProjectPodcastSerializer)


class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class Categories(viewsets.ModelViewSet):
    permission_classes = (ReadOnlyPermission,)


class NewsCategories(Categories):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer


class RadioCategories(Categories):
    queryset = RadioCategory.objects.all()
    serializer_class = RadioCategorySerializer


class ProjectCategories(Categories):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer


class Shows(viewsets.ModelViewSet):
    permission_classes = (ReadOnlyPermission,)


class NewsShows(Shows):
    queryset = NewsShow.objects.all()
    serializer_class = NewsShowSerializer


class RadioShows(Shows):
    queryset = RadioShow.objects.all()
    serializer_class = RadioShowSerializer


class ProjectShows(Shows):
    queryset = ProjectShow.objects.all()
    serializer_class = ProjectShowSerializer


class Podcasts(viewsets.ModelViewSet):
    permission_classes = (ReadOnlyPermission,)


class NewsPodcasts(Podcasts):
    queryset = NewsPodcast.objects.all()
    serializer_class = NewsPodcastSerializer


class RadioPodcasts(Podcasts):
    queryset = RadioPodcast.objects.all()
    serializer_class = RadioPodcastSerializer


class ProjectPodcasts(Podcasts):
    queryset = ProjectPodcast.objects.all()
    serializer_class = ProjectPodcastSerializer
