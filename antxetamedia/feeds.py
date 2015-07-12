import itertools

from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _

from news.models import NewsPodcast
from radio.models import RadioPodcast


######
# BIG TODO QUESTION: PodcastFeed or BlobFeed??
######

class PodcastFeed(Feed):
    title = _('Latest podcasts')
    description = _('Latest news and radio podcasts from Antxetamedia')
    link = '/'
    author_name = 'Antxeta Irratia'

    def feed_url(self):
        return reverse('feed')

    def items(self):
        # We must get the user's favourite podcasts here
        newspodcasts = NewsPodcast.objects.published()[:10]
        radiopodcasts = RadioPodcast.objects.published()[:10]
        items = itertools.chain(newspodcasts, radiopodcasts)
        return sorted(items, key='pub_date')

    def item_title(self, item):
        return item.title

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

    # TODO: enclosure stuff, check if multiple enclosures are possible
    def item_enclosure_url(self, item):
        pass

    def item_enclosure_length(self, item):
        pass

    def item_enclosure_mime_type(self, item):
        pass


