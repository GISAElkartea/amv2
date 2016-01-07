import itertools
from operator import attrgetter

from django.contrib.syndication.views import Feed, add_domain
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed, Enclosure
from django.utils.translation import ugettext_lazy as _

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast


class BlobFeed(Feed):
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
        return sorted(items, key=attrgetter('pub_date'))

    def item_title(self, item):
        return str(item)

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return item.show.name

    def item_author_link(self, item):
        return item.show.get_absolute_url()

    def item_enclosures(self, item):
        for blob in item.blob_set.all():
            if blob.link:
                # add_domain adds the domain only if the url doesn't already have one
                link = add_domain(self.request.get_host(), blob.link, self.request.is_secure())
                # When an enclosure's size cannot be determined, a publisher should use a length of 0.
                yield Enclosure(link, length='0', mime_type="audio/mpeg")
