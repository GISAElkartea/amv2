import itertools
from operator import attrgetter

from django.contrib.syndication.views import Feed, add_domain
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast


class BlobFeed(Feed):
    # It looks like multiple enclosure support for Atom feeds is coming:
    # https://code.djangoproject.com/ticket/13110
    feed_type = Atom1Feed
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
        newspodcasts = NewsPodcast.objects.published()[:10]
        radiopodcasts = RadioPodcast.objects.published()[:10]
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
        # Atom feeds can contain more than one enclosure while RSS feeds can not.
        # There is a ticket to accept more than one enclosure for Atom feeds:
        # https://code.djangoproject.com/ticket/13110
        if item.link:
            # add_domain adds the domain only if the url doesn't already have one
            return add_domain(self.request.get_host(), item.link, self.request.is_secure())

    def item_enclosure_length(self, item):
        # When an enclosure's size cannot be determined, a publisher should use a length of 0.
        return 0  #

    def item_enclosure_mime_type(self, item):
        return "audio/mpeg"
