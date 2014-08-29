from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import (NewsCategory, RadioCategory, ProjectCategory,
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


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)


class NewsCategoryViewSet(CategoryViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer


class RadioCategoryViewSet(CategoryViewSet):
    queryset = RadioCategory.objects.all()
    serializer_class = RadioCategorySerializer


class ProjectCategoryViewSet(CategoryViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer


class ShowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)


class NewsShowViewSet(ShowViewSet):
    queryset = NewsShow.objects.all()
    serializer_class = NewsShowSerializer


class RadioShowViewSet(ShowViewSet):
    queryset = RadioShow.objects.all()
    serializer_class = RadioShowSerializer


class ProjectShowViewSet(ShowViewSet):
    queryset = ProjectShow.objects.all()
    serializer_class = ProjectShowSerializer


class PodcastViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)


class NewsPodcastViewSet(PodcastViewSet):
    queryset = NewsPodcast.objects.all()
    serializer_class = NewsPodcastSerializer


class RadioPodcastViewSet(PodcastViewSet):
    queryset = RadioPodcast.objects.all()
    serializer_class = RadioPodcastSerializer


class ProjectPodcastViewSet(PodcastViewSet):
    queryset = ProjectPodcast.objects.all()
    serializer_class = ProjectPodcastSerializer
