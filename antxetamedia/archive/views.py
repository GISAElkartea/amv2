from django.views.generic import ListView

import watson
from watson.views import SearchMixin as WatsonSearchView

from .filtersets import NewsPodcastFilterSet, RadioPodcastFilterSet, ProjectShowFilterSet


class SearchMixin(WatsonSearchView):
    template_name = 'archive/search.html'
    paginate_by = 10


class SingleModelSearchMixin(SearchMixin):
    def get_base_queryset(self):
        return self.queryset

    def get_queryset(self):
        return watson.filter(self.get_base_queryset(), self.query)


class FilterSetSeachMixin(SingleModelSearchMixin):
    filterset_class = None

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = self.filterset_class(self.request.GET).form
        return super(FilterSetSeachMixin, self).get_context_data(*args, **kwargs)

    def get_queryset(self):
        filterset = self.filterset_class(self.request.GET, queryset=self.get_base_queryset())
        return watson.filter(filterset.qs, self.query)


class SearchView(SearchMixin, ListView):
    pass


class NewsPodcastSearchView(FilterSetSeachMixin, ListView):
    filterset_class = NewsPodcastFilterSet


class RadioPodcastSearchView(FilterSetSeachMixin, ListView):
    filterset_class = RadioPodcastFilterSet


class ProjectShowSearchView(FilterSetSeachMixin, ListView):
    filterset_class = ProjectShowFilterSet
