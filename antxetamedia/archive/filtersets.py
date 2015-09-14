from django.utils.translation import ugettext_lazy as _

from django_filters import FilterSet, DateFilter, DateTimeFilter

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast
from antxetamedia.projects.models import ProjectShow
from .forms import PikadayDateField, PikadayDateTimeHiddenTimeField


class PikadayDateFilter(DateFilter):
    field_class = PikadayDateField


class PikadayDateTimeFilter(DateTimeFilter):
    field_class = PikadayDateTimeHiddenTimeField


# We do not want to accidentally discard anything, so be inclusive and always
# make gte and lte lookups instead of using gt or lt ones


class NewsPodcastFilterSet(FilterSet):
    pub_date_after = PikadayDateTimeFilter('pub_date', lookup_type='gte', label=_('Published after'))
    pub_date_before = PikadayDateTimeFilter('pub_date', lookup_type='lte', label=_('Published before'))

    class Meta:
        model = NewsPodcast
        fields = ['show', 'categories', 'pub_date_after', 'pub_date_before']


class RadioPodcastFilterSet(FilterSet):
    pub_date_after = PikadayDateTimeFilter('pub_date', lookup_type='gte', label=_('Published after'))
    pub_date_before = PikadayDateTimeFilter('pub_date', lookup_type='lte', label=_('Published before'))

    class Meta:
        model = RadioPodcast
        fields = ['show', 'show__category', 'show__producer', 'pub_date_after', 'pub_date_before']


class ProjectShowFilterSet(FilterSet):
    creation_date = PikadayDateFilter('creation_date', lookup_type='year__exact', label=_('Creation date'))

    class Meta:
        model = ProjectShow
        fields = ['producer', 'creation_date']
