from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import Playlist, PlaylistElement
from .serializers import PlaylistSerializer, PlaylistElementSerializer


class OwnerPermissionPlaylist(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class OwnerFilterPlaylist(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class UserPlaylists(NestedViewSetMixin, viewsets.ModelViewSet):
    model = Playlist
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated, OwnerPermissionPlaylist)
    filter_backends = (OwnerFilterPlaylist,)

    def pre_save(self, obj):
        obj.user = self.request.user


class OwnerPermissionElement(permissions.BasePermission):
    def has_permission(self, request, view):
        playlist = view.kwargs.get('parent_lookup_playlist')
        return Playlist.objects.filter(pk=playlist, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return request.user == obj.playlist.user


class PlaylistElements(NestedViewSetMixin, viewsets.ModelViewSet):
    model = PlaylistElement
    serializer_class = PlaylistElementSerializer
    permission_classes = (IsAuthenticated, OwnerPermissionElement,)

    def pre_save(self, obj):
        obj.playlist.user = self.request.user
