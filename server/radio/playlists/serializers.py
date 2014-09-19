from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models import Playlist, PlaylistElement


class TagListSerializer(serializers.WritableField):
    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class PlaylistElementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='podcast.id')
    title = serializers.CharField(source='podcast.title')
    description = serializers.CharField(source='podcast.description',
                                        required=False)
    image = serializers.ImageField(source='podcast.image', required=False)
    tags = TagListSerializer(source='podcast.tags', blank=True)

    class Meta:
        model = PlaylistElement
        fields = ('position', 'id', 'title', 'description', 'image', 'tags')


class PlaylistSerializer(serializers.ModelSerializer):
    podcasts = PlaylistElementSerializer(source='elements', many=True,
                                         required=False)

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'podcasts')
