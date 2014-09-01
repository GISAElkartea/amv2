from django.core.urlresolvers import reverse
from django.utils.six import text_type as str

from rest_framework.test import APITestCase
from rest_framework import status
from model_mommy import mommy

from ..serializers import PlaylistPodcastSerializer


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = mommy.make('User')
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()


class UsersPlaylistListTestCase(UserTestCase):
    def setUp(self):
        super(UsersPlaylistListTestCase, self).setUp()
        self.url = reverse('playlist-list')
        self.news_podcasts = mommy.make('NewsPodcast')
        self.radio_podcasts = mommy.make('RadioPodcast')
        self.project_podcast = mommy.make('ProjectPodcast')
        self.podcasts = [self.news_podcasts,
                         self.radio_podcasts,
                         self.project_podcast]

    def test_no_playlists(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_no_user_playlist(self):
        other_user = mommy.make('User')
        mommy.make('Playlist', user=other_user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_no_podcast(self):
        playlist = mommy.make('Playlist', user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': playlist.id,
            'title': playlist.title,
            'podcasts': [],
        }])

    def test_single_podcast(self):
        for podcast in self.podcasts:
            playlist = mommy.make('Playlist', user=self.user)
            position = mommy.make('PlaylistPosition', playlist=playlist,
                                  podcast=podcast)
            response = self.client.get(self.url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn({
                'id': playlist.id,
                'title': playlist.title,
                'podcasts': [{
                    'id': position.podcast.id,
                    'position': position.position,
                    'title': position.podcast.title,
                    'description': position.podcast.description,
                    'image': str(position.podcast.image),
                    'tags': list(position.podcast.tags.all()),
                }],
            }, response.data)

    def test_multiple_podcats(self):
        playlist = mommy.make('Playlist', user=self.user)
        for podcast in self.podcasts:
            mommy.make('PlaylistPosition', playlist=playlist, podcast=podcast)
        positions = playlist.ordering.all()
        podcasts = PlaylistPodcastSerializer(positions, many=True).data
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': playlist.id,
            'title': playlist.title,
            'podcasts': podcasts,
        }])


    #def test_create_users_playlist(self):
        #playlist = mommy.prepare('Playlist')
        #url = reverse('playlist-list')
        #response = self.client.post(url, PlaylistSerializer(playlist).data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #desired = PlaylistSerializer(playlist).data
        #desired.pop('id')
        #response.data.pop('id')
        #self.assertEqual(response.data, desired)

    #def test_delete_users_playlist(self):
        #pass
