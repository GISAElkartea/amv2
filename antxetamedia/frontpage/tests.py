import mock
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, override_settings

from antxetamedia.frontpage.views import FrontPage, ConfigureFrontPage


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
        objects.all.assert_called_once_with()

    def test_correct_order(self):
        view = view_instance(FrontPage, self.request)
        qs = view.get_context_data()['widget_list']
        ordering = qs.model._meta.ordering if qs.query.default_ordering else qs.query.order_by
        self.assertEqual(ordering, ['position'])


class FrontPageConfigurationTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('configure-frontpage'))
        self.newscategories = [6, 102, 23845, 21]
        self.radioshows = [1, 86, 93]

    def test_cookies_in_form_initial_data(self):
        self.request.COOKIES[settings.NEWSCATEGORIES_COOKIE] = json.dumps(self.newscategories)
        self.request.COOKIES[settings.RADIOSHOWS_COOKIE] = json.dumps(self.radioshows)
        view = view_instance(ConfigureFrontPage, self.request)
        form = view.get_form()
        self.assertEqual(form.initial['newscategories'], self.newscategories)
        self.assertEqual(form.initial['radioshows'], self.radioshows)

    @mock.patch('antxetamedia.radio.models.RadioShow.objects')
    @mock.patch('antxetamedia.news.models.NewsCategory.objects')
    def test_form_initial_data_without_cookies(self, NewsCategoryQS, RadioShowQS):
        NewsCategoryQS.values_list.return_value = self.newscategories
        RadioShowQS.values_list.return_value = self.radioshows
        view = view_instance(ConfigureFrontPage, self.request)
        form = view.get_form()
        self.assertEqual(form.initial['newscategories'], self.newscategories)
        self.assertEqual(form.initial['radioshows'], self.radioshows)

    @mock.patch('antxetamedia.radio.models.RadioShow.objects')
    @mock.patch('antxetamedia.news.models.NewsCategory.objects')
    def test_form_selection_sets_cookies(self, NewsCategoryQS, RadioShowQS):
        request = RequestFactory().post(reverse('configure-frontpage'), {
            'newscategories': self.newscategories,
            'radioshows': self.radioshows,
        })
        NewsCategoryQS.configure_mock(**{'values_list.return_value': self.newscategories,
                                         'iterator.return_value': self.newscategories})
        RadioShowQS.configure_mock(**{'values_list.return_value': self.radioshows,
                                      'iterator.return_value': self.radioshows})
        response = ConfigureFrontPage.as_view()(request)
        NewsCategoryQS.values_list.assert_called_once_with('pk', flat=True)
        RadioShowQS.values_list.assert_called_once_with('pk', flat=True)
