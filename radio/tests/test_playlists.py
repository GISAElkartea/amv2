from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.utils.six import text_type as str

from rest_framework.test import APITestCase
from rest_framework import status
from model_mommy import mommy

from ..models import Playlist
from ..serializers import PlaylistElementSerializer


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = mommy.make('User')
        self.authenticate()

    def authenticate(self):
        self.client.force_authenticate(self.user)

    def deauthenticate(self):
        self.client.force_authenticate(AnonymousUser())

    def tearDown(self):
        self.client.logout()


class UsersPlaylistListTestCase(UserTestCase):
    url = reverse('playlist-list')

    def setUp(self):
        super(UsersPlaylistListTestCase, self).setUp()
        self.news_podcasts = mommy.make('NewsPodcast')
        self.radio_podcasts = mommy.make('RadioPodcast')
        self.project_podcast = mommy.make('ProjectPodcast')
        self.podcasts = [self.news_podcasts,
                         self.radio_podcasts,
                         self.project_podcast]

    def test_forbidden_for_anonymous(self):
        self.deauthenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_playlists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_no_user_playlist(self):
        other_user = mommy.make('User')
        mommy.make('Playlist', user=other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_no_podcast(self):
        playlist = mommy.make('Playlist', user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': playlist.id,
            'title': playlist.title,
            'podcasts': [],
        }])

    def test_single_podcast(self):
        for podcast in self.podcasts:
            playlist = mommy.make('Playlist', user=self.user)
            element = mommy.make('PlaylistElement', playlist=playlist, podcast=podcast)
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn({
                'id': playlist.id,
                'title': playlist.title,
                'podcasts': [{
                    'id': element.podcast.id,
                    'position': element.position,
                    'title': element.podcast.title,
                    'description': element.podcast.description,
                    'image': str(element.podcast.image),
                    'tags': list(element.podcast.tags.all()),
                }],
            }, response.data)

    def test_multiple_podcats(self):
        playlist = mommy.make('Playlist', user=self.user)
        for podcast in self.podcasts:
            mommy.make('PlaylistElement', playlist=playlist, podcast=podcast)
        elements = playlist.elements.all()
        podcasts = PlaylistElementSerializer(elements, many=True).data
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': playlist.id,
            'title': playlist.title,
            'podcasts': podcasts,
        }])

    def test_podcast_order(self):
        playlist = mommy.make('Playlist', user=self.user)
        for podcast in self.podcasts:
            mommy.make('PlaylistElement', playlist=playlist, podcast=podcast)
        response = self.client.get(self.url)
        podcasts = response.data[0]['podcasts']
        positions = [podcast['position'] for podcast in podcasts]
        self.assertEqual(positions, sorted(positions))


class UserPlaylistCreateTestCase(UserTestCase):
    url = reverse('playlist-list')

    def test_forbidden_for_anonymous(self):
        self.deauthenticate()
        response = self.client.post(self.url, {'title': 'example'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_playlist_creation(self):
        response = self.client.post(self.url, {'title': 'example'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_binded_to_playlist(self):
        self.client.post(self.url, {'title': 'example'})
        playlist = Playlist.objects.get(title='example')
        self.assertEqual(playlist.user, self.user)


class UserPlaylistUpdateTestCase(UserTestCase):
    def test_forbidden_for_anonymous(self):
        self.deauthenticate()
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_absolute_url()
        response = self.client.put(url, {'title': 'example'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_users_can_not_modify(self):
        owner = mommy.make('User')
        playlist = mommy.make('Playlist', user=owner)
        url = playlist.get_absolute_url()
        response = self.client.put(url, {'title': 'changed'})
        playlist = Playlist.objects.get(pk=playlist.pk)
        self.assertNotEqual(playlist.title, response.data['title'])

    def test_owner_can_modify(self):
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_absolute_url()
        response = self.client.put(url, {'title': 'changed'})
        playlist = Playlist.objects.get(pk=playlist.pk)
        self.assertEqual(playlist.title, response.data['title'])


class UserPlaylistDeleteTestCase(UserTestCase):
    def test_forbidden_for_anonymous(self):
        self.deauthenticate()
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_absolute_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_users_can_not_delete(self):
        owner = mommy.make('User')
        playlist = mommy.make('Playlist', user=owner)
        url = playlist.get_absolute_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete(self):
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_absolute_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PodcastListTestCase(UserTestCase):
    def setUp(self):
        super(PodcastListTestCase, self).setUp()
        self.playlist = mommy.make('Playlist', user=self.user)
        self.url = self.playlist.get_absolute_url()

    def test_forbidden_for_anonymous(self):
        self.deauthenticate()
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_podcasts_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_users_can_not_list(self):
        owner = mommy.make('User')
        playlist = mommy.make('Playlist', user=owner)
        url = playlist.get_podcasts_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_list(self):
        playlist = mommy.make('Playlist', user=self.user)
        url = playlist.get_podcasts_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_podcast_order(self):
        news_podcasts = mommy.make('NewsPodcast')
        radio_podcasts = mommy.make('RadioPodcast')
        project_podcast = mommy.make('ProjectPodcast')
        podcasts = [news_podcasts, radio_podcasts, project_podcast]
        for podcast in podcasts:
            mommy.make('PlaylistElement', playlist=self.playlist,
                       podcast=podcast)
