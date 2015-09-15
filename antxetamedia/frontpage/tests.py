from unittest import mock

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, override_settings

from antxetamedia.frontpage.views import FrontPage


def view_instance(ViewClass, request, *args, **kwargs):
    view = ViewClass()
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class NewsPodcastsInFrontPage(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('frontpage'))

    def test_context_present(self):
        view = view_instance(FrontPage, self.request)
        self.assertIn('newspodcast_list', view.get_context_data())

    @mock.patch('antxetamedia.news.models.NewsPodcast.objects')
    def test_quantity(self, objects):
        view = view_instance(FrontPage, self.request)
        with override_settings(FRONTPAGE_NEWSPODCASTS=mock.sentinel.quantity):
            view.get_context_data()
        objects.favourites.assert_called_once_with(self.request)
        objects.favourites().__getitem__.assert_called_once_with(slice(None, mock.sentinel.quantity, None))

    def test_correct_order(self):
        view = view_instance(FrontPage, self.request)
        qs = view.get_context_data()['newspodcast_list']
        ordering = qs.model._meta.ordering if qs.query.default_ordering else qs.query.order_by
        self.assertEqual(ordering, ['-featured', '-pub_date'])


class RadioPodcastsInFrontPage(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('frontpage'))

    def test_context_present(self):
        view = view_instance(FrontPage, self.request)
        self.assertIn('radiopodcast_list', view.get_context_data())

    @mock.patch('antxetamedia.radio.models.RadioPodcast.objects')
    def test_quantity(self, objects):
        view = view_instance(FrontPage, self.request)
        with override_settings(FRONTPAGE_RADIOPODCASTS=mock.sentinel.quantity):
            view.get_context_data()
        objects.favourites.assert_called_once_with(self.request)
        objects.favourites().__getitem__.assert_called_once_with(slice(None, mock.sentinel.quantity, None))

    def test_correct_order(self):
        view = view_instance(FrontPage, self.request)
        qs = view.get_context_data()['radiopodcast_list']
        ordering = qs.model._meta.ordering if qs.query.default_ordering else qs.query.order_by
        self.assertEqual(ordering, ['-pub_date'])


class EventsInFrontPage(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('frontpage'))

    def test_context_present(self):
        view = view_instance(FrontPage, self.request)
        self.assertIn('event_list', view.get_context_data())

    @mock.patch('antxetamedia.events.models.Event.objects')
    def test_quantity(self, objects):
        view = view_instance(FrontPage, self.request)
        with override_settings(FRONTPAGE_EVENTS=mock.sentinel.quantity):
            view.get_context_data()
        objects.upcoming.assert_called_once_with(count=mock.sentinel.quantity)


class WidgetsInFrontPage(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('frontpage'))

    def test_context_present(self):
        view = view_instance(FrontPage, self.request)
        self.assertIn('widget_list', view.get_context_data())

    @mock.patch('antxetamedia.widgets.models.Widget.objects')
    def test_quantity(self, objects):
        view = view_instance(FrontPage, self.request)
        view.get_context_data()
        objects.all.assert_called_once_with(self.request)

    def test_correct_order(self):
        view = view_instance(FrontPage, self.request)
        qs = view.get_context_data()['widget_list']
        ordering = qs.model._meta.ordering if qs.query.default_ordering else qs.query.order_by
        self.assertEqual(ordering, ['-position'])
