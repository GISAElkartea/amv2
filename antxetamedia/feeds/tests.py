from django.core.urlresolvers import reverse

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from antxetamedia.tests import blob


class FeedTestCase(TestCase):
    def setUp(self):
        self.url = reverse('feed')

    @given(st.list(blob))
    def test_status_code(self, blobs):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @given(st.list(blob))
    def test_enclosure(self, blobs):
        pass
