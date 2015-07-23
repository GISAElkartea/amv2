from itertools import islice

from django.core.urlresolvers import reverse
from django.test import override_settings

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast
from antxetamedia.events.models import Event
from antxetamedia.widgets.models import Widget
from antxetamedia.tests import newspodcast, radiopodcast, event, widget


class NewsPodcastsInFrontPage(TestCase):
    def setUp(self):
        self.url = reverse('frontpage')

    def test_context_present(self):
        """
        Test that the frontpage has the news podcast list in its context.
        """
        response = self.client.get(self.url)
        self.assertIn('newspodcast_list', response.context)

    @given(st.lists(newspodcast), st.integers(min_value=0))
    def test_correct_number_of_newspodcasts(self, newspodcasts, limit):
        """
        Test that the number of news podcasts on the frontpage doesn't exceed
        the maximum allowed and, if less, equals the number of news podcasts.
        """
        with override_settings(FRONTPAGE_NEWSPODCASTS=limit):
            response = self.client.get(self.url)
            expected = max(NewsPodcast.objects.published().count(), limit)
            self.assertLessEqual(response.context['newspodcast_list'].count(), expected)

    @given(st.lists(newspodcast))
    def test_correct_order_of_newspodcasts(self, newspodcasts):
        """
        Test that the podcasts on the frontpage are ordered by their pub date,
        the most recent first.
        """
        response = self.client.get(self.url)
        newspodcasts = list(response.context['newspodcast_list'])
        for i in range(len(newspodcasts) - 1):
            self.assertTrue(newspodcasts[i].pub_date >= newspodcasts[i + 1].pub_date)


class RadioPodcastsInFrontPage(TestCase):
    def setUp(self):
        self.url = reverse('frontpage')

    def test_context_present(self):
        response = self.client.get(self.url)
        self.assertIn('radiopodcast_list', response.context)

    @given(st.lists(radiopodcast), st.integers(min_value=0))
    def test_correct_number_of_radiopodcasts(self, radiopodcasts, limit):
        with override_settings(FRONTPAGE_RADIOPODCASTS=limit):
            response = self.client.get(self.url)
            expected = max(RadioPodcast.objects.published().count(), limit)
            self.assertLessEqual(response.context['radiopodcast_list'].count(), expected)

    @given(st.lists(radiopodcast))
    def test_correct_order_of_radiopodcasts(self, radiopodcasts):
        response = self.client.get(self.url)
        radiopodcasts = list(response.context['radiopodcast_list'])
        for i in range(len(radiopodcasts) - 1):
            self.assertTrue(radiopodcasts[i].pub_date >= radiopodcasts[i + 1].pub_date)


class EventsInFrontPage(TestCase):
    def setUp(self):
        self.url = reverse('frontpage')

    def test_context_present(self):
        response = self.client.get(self.url)
        self.assertIn('event_list', response.context)

    @given(st.lists(event), st.integers(min_value=0))
    def test_correct_number_of_events(self, events, limit):
        with override_settings(FRONTPAGE_EVENTS=limit):
            response = self.client.get(self.url)
            expected = list(islice(Event.objects.upcoming(), limit))
            actual = list(response.context['event_list'])
            self.assertEqual(len(actual), len(expected))

    @given(st.lists(event))
    def test_correct_order_of_events(self, events):
        response = self.client.get(self.url)
        events = list(response.context['event_list'])
        for i in range(len(events) - 1):
            current = next(events[i].upcoming())
            following = next(events[i + 1].upcoming())
            self.assertLessEqual(current, following)


class WidgetsInFrontPage(TestCase):
    def setUp(self):
        self.url = reverse('frontpage')

    def test_context_present(self):
        response = self.client.get(self.url)
        self.assertIn('widget_list', response.context)

    @given(st.lists(widget))
    def test_all_widgets(self, widgets):
        response = self.client.get(self.url)
        expected = Widget.objects.all()
        actual = response.context['widget_list']
        self.assertEqual(len(actual), len(expected))

    @given(st.lists(widget))
    def test_correct_order_of_widgets(self, widgets):
        response = self.client.get(self.url)
        widgets = response.context['widget_list']
        for i in range(len(widgets) - 1):
            self.assertLessEqual(widgets[i].position, widgets[i + 1].position)
