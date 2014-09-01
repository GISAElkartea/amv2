from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import (NewsCategory, RadioCategory, ProjectCategory,
                     NewsShow, RadioShow, ProjectShow,
                     NewsPodcast, RadioPodcast, ProjectPodcast,
                     Playlist, PlaylistPosition)


class TagListSerializer(serializers.WritableField):
    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name',)


class NewsCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        model = NewsCategory


class RadioCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        model = RadioCategory


class ProjectCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        model = ProjectCategory


class ShowSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(blank=True)

    class Meta:
        fields = ('id', 'name', 'description', 'image', 'categories', 'tags')


class NewsShowSerializer(ShowSerializer):
    class Meta(ShowSerializer.Meta):
        model = NewsShow


class RadioShowSerializer(ShowSerializer):
    class Meta(ShowSerializer.Meta):
        model = RadioShow


class ProjectShowSerializer(ShowSerializer):
    class Meta(ShowSerializer.Meta):
        model = ProjectShow


class PodcastSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(blank=True)

    class Meta:
        fields = ('id', 'title', 'description', 'image', 'tags')


class NewsPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = NewsPodcast


class RadioPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = RadioPodcast


class ProjectPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = ProjectPodcast


class PlaylistPodcastSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='podcast.id')
    title = serializers.CharField(source='podcast.title')
    description = serializers.CharField(source='podcast.description',
                                        required=False)
    image = serializers.ImageField(source='podcast.image', required=False)
    tags = TagListSerializer(source='podcast.tags', blank=True)

    class Meta:
        model = PlaylistPosition
        fields = ('position', 'id', 'title', 'description', 'image', 'tags')


class PlaylistSerializer(serializers.ModelSerializer):
    podcasts = PlaylistPodcastSerializer(source='ordering', many=True,
                                         required=False)

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'podcasts')
