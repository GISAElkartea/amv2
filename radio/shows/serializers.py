from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models import (NewsCategory, RadioCategory, ProjectCategory,
                      NewsShow, RadioShow, ProjectShow,
                      NewsPodcast, RadioPodcast, ProjectPodcast)


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
    categories = NewsCategorySerializer(many=True)

    class Meta(ShowSerializer.Meta):
        model = NewsShow


class RadioShowSerializer(ShowSerializer):
    categories = RadioCategorySerializer(many=True)

    class Meta(ShowSerializer.Meta):
        model = RadioShow


class ProjectShowSerializer(ShowSerializer):
    categories = ProjectCategorySerializer(many=True)

    class Meta(ShowSerializer.Meta):
        model = ProjectShow


class PodcastSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(blank=True)

    class Meta:
        fields = ('id', 'title', 'description', 'image', 'tags', 'show')


class NewsPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = NewsPodcast


class RadioPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = RadioPodcast


class ProjectPodcastSerializer(PodcastSerializer):
    class Meta(PodcastSerializer.Meta):
        model = ProjectPodcast
