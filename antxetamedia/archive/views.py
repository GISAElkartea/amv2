from functools import reduce
from operator import add

from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.utils.translation import ugettext as _

import watson
from watson.views import SearchMixin as WatsonSearchView

from antxetamedia.events.models import Event
from .filtersets import NewsPodcastFilterSet, RadioPodcastFilterSet, ProjectShowFilterSet
from .forms import EventForm


class SearchMixin(WatsonSearchView):
    template_name = 'archive/search.html'
    paginate_by = 10

    def get_tabs(self):
        return [
            (_('Site-wide'), reverse('archive:search'), None),
            (_('News podcasts'), reverse('archive:news'), NewsPodcastFilterSet(self.request.GET).form),
            (_('Radio podcasts'), reverse('archive:radio'), RadioPodcastFilterSet(self.request.GET).form),
            (_('Projects'), reverse('archive:projects'), ProjectShowFilterSet(self.request.GET).form),
            (_('Events'), reverse('archive:events'), EventForm(self.request.GET)),
        ]

    def get_context_data(self, **kwargs):
        tabs = self.get_tabs()
        kwargs['tabs'] = tabs
        # Union of all media files
        kwargs['tab_media'] = reduce(add, [form.media for name, url, form in tabs if form is not None])
        return super(SearchMixin, self).get_context_data(**kwargs)


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


class EventSearchView(FormMixin, SingleModelSearchMixin, ListView):
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        self.query = self.get_query(request)
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_base_queryset(self):
        return Event.objects.all()

    def get_initial(self):
        return self.request.GET

    def get_form_kwargs(self):
        kwargs = super(EventSearchView, self).get_form_kwargs()
        kwargs['data'] = self.request.GET
        return kwargs

    def form_valid(self, form):
        after = form.cleaned_data.get('after')
        before = form.cleaned_data.get('before')
        # NOTE: Little hack, event generator can be infinite, limit it to 10 pages
        count = self.paginate_by * 10
        qs = self.get_queryset()
        if (after, before) != (None, None):
            if None not in (after, before):
                qs = qs.between(after, before, count=count)
            elif after is not None:
                qs = qs.after(after, count=count)
            elif before is not None:
                qs = qs.before(before, count=count)
            qs = list({event for date, event in qs})
        self.object_list = qs
        return self.render_to_response(self.get_context_data(form=self.get_form()))
