from rest_framework import serializers

from .models import (NewsCategory, RadioCategory, ProjectCategory,
                     NewsShow, RadioShow, ProjectShow,
                     NewsPodcast, RadioPodcast, ProjectPodcast,
                     Playlist, PlaylistPosition)


class GenericObjectRelatedField(serializers.RelatedField):
    def __init__(self, *args, **kwargs):
        self.related_serializers = kwargs.pop('related_serializers', None)
        super(GenericObjectRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        Serializer = self.related_serializers[value.__class__]
        serialized = Serializer(value)
        return serialized.data


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


class PlaylistPositionSerializer(serializers.ModelSerializer):
    podcast = GenericObjectRelatedField(related_serializers={
        NewsPodcast: NewsPodcastSerializer,
        RadioPodcast: RadioPodcastSerializer,
        ProjectPodcast: ProjectPodcastSerializer,
    })

    class Meta:
        model = PlaylistPosition
        fields = ('id', 'podcast', 'position')


class PlaylistSerializer(serializers.ModelSerializer):
    ordering = PlaylistPositionSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'user', 'ordering')
