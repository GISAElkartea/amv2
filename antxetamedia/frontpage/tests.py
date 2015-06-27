from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from model_mommy import mommy

from .views import VISITED_COOKIE, VISITED_COOKIE_VALUE


User = get_user_model()


class WelcomePageTestCase(TestCase):
    def test_visited_cookie_set_if_not_present(self):
        response = self.client.get(reverse('welcomepage'))
        self.assertIn(VISITED_COOKIE, response.cookies)
        self.assertEqual(response.cookies[VISITED_COOKIE].value, VISITED_COOKIE_VALUE)


class FrontPageTestCase(TestCase):
    def setUp(self):
        self.url = reverse('frontpage')
        self.credentials = {'username': 'username', 'password': 'password'}
        self.user = User.objects.create_user(**self.credentials)

    def test_no_redirect_if_authenticated(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_if_visited_cookie(self):
        self.client.cookies[VISITED_COOKIE] = VISITED_COOKIE_VALUE
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_authenticated_and_not_visited_cookie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_context_present(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertIn('newspodcast_list', response.context)
        self.assertIn('radiopodcast_list', response.context)
        self.assertIn('event_list', response.context)
        self.assertIn('widget_list', response.context)

    def test_no_other_users_favourite_newspodcasts(self):
        normal = mommy.make('news.NewsShow')
        favourite = mommy.make('favourites.FavouriteNewsShow')
        normal_podcast = mommy.make('news.NewsPodcast', show=normal)
        favourite_podcast = mommy.make('news.NewsPodcast', show=favourite.show)
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertIn(normal_podcast, response.context['newspodcast_list'])
        self.assertIn(favourite_podcast, response.context['newspodcast_list'])

    def test_users_favourite_newspodcasts(self):
        normal = mommy.make('news.NewsShow')
        favourite = mommy.make('favourites.FavouriteNewsShow', user=self.user)
        normal_podcast = mommy.make('news.NewsPodcast', show=normal)
        favourite_podcast = mommy.make('news.NewsPodcast', show=favourite.show)
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertNotIn(normal_podcast, response.context['newspodcast_list'])
        self.assertIn(favourite_podcast, response.context['newspodcast_list'])

    def test_no_other_users_favourite_radiopodcasts(self):
        normal = mommy.make('radio.RadioShow')
        favourite = mommy.make('favourites.FavouriteRadioShow')
        normal_podcast = mommy.make('radio.RadioPodcast', show=normal)
        favourite_podcast = mommy.make('radio.RadioPodcast', show=favourite.show)
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertIn(normal_podcast, response.context['radiopodcast_list'])
        self.assertIn(favourite_podcast, response.context['radiopodcast_list'])

    def test_users_favourite_radiopodcasts(self):
        normal = mommy.make('radio.RadioShow')
        favourite = mommy.make('favourites.FavouriteRadioShow', user=self.user)
        normal_podcast = mommy.make('radio.RadioPodcast', show=normal)
        favourite_podcast = mommy.make('radio.RadioPodcast', show=favourite.show)
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertNotIn(normal_podcast, response.context['radiopodcast_list'])
        self.assertIn(favourite_podcast, response.context['radiopodcast_list'])
