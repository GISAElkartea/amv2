import itertools
from operator import attrgetter

from django.contrib.syndication.views import Feed, add_domain
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast


class BlobFeed(Feed):
    title = _('Latest podcasts from Antxetamedia')
    description = _('Latest news and radio podcasts from Antxetamedia')
    link = '/'
    author_name = 'Antxeta Irratia'

    def get_feed(self, obj, request):
        self.request = request
        return super(BlobFeed, self).get_feed(obj, request)

    def feed_url(self):
        return reverse('feed')

    def items(self):
        # Blobs do not have a creation timestamp. We must therefore get the
        # podcasts, order them, and get their related blobs
        newspodcasts = NewsPodcast.objects.published().favourites(self.request)[:10]
        radiopodcasts = RadioPodcast.objects.published().favourites(self.request)[:10]
        items = itertools.chain(newspodcasts, radiopodcasts)
        for item in sorted(items, key=attrgetter('pub_date')):
            for blob in item.blob_set.all():
                yield blob

    def item_title(self, item):
        return str(item)

    def item_description(self, item):
        return item.content_object.description

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def item_pubdate(self, item):
        return item.content_object.pub_date

    def item_author_name(self, item):
        return item.content_object.show.name

    def item_author_link(self, item):
        return item.content_object.show.get_absolute_url()

    def item_enclosure_url(self, item):
        if item.blob:
            return add_domain(self.request.get_host(), item.blob, self.request.is_secure())

    def item_enclosure_length(self, item):
        # Is this really needed?
        pass

    def item_enclosure_mime_type(self, item):
        return "audio/mpeg"
