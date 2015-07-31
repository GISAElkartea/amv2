from django_filters import FilterSet

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast
from antxetamedia.projects.models import ProjectShow
from antxetamedia.events.models import Event


# We do not want to accidentally discard anything, so be inclusive and always
# make gte and lte lookups instead of using gt or lt ones


class NewsPodcastFilterSet(FilterSet):
    class Meta:
        model = NewsPodcast
        fields = {
            'show': ['exact'],
            'categories': ['exact'],
            'pub_date': ['gte', 'lte'],
        }


class RadioPodcastFilterSet(FilterSet):
    class Meta:
        model = RadioPodcast
        fields = {
            'show': ['exact'],
            'show__category': ['exact'],
            'show__producer': ['exact'],
            'pub_date': ['gte', 'lte'],
        }


class ProjectShowFilterSet(FilterSet):
    class Meta:
        model = ProjectShow
        fields = {
            'producer': ['exact'],
            'creation_date': ['year__exact'],
        }


class EventFilterSet(FilterSet):
    class Meta:
        model = Event
