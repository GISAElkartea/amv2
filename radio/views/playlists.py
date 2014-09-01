from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Playlist, PlaylistPosition
from ..serializers import PlaylistSerializer, PlaylistPodcastSerializer


class UserPlaylists(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    def pre_save(self, obj):
        obj.user = self.request.user


class PlaylistPositions(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistPodcastSerializer

    def get_playlist(self):
        playlist = self.request.QUERY_PARAMS.get('playlist')
        return get_object_or_404(Playlist, pk=playlist, user=self.request.user)

    def get_queryset(self):
        return PlaylistPosition.objects.filter(playlist=self.get_playlist())

    def pre_save(self, obj):
        obj.playlist = self.get_playlist()
        obj.user = self.request.user
