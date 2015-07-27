from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import NewsPodcast, NewsShow, NewsCategory
from .forms import NewsPodcastFilter


class NewsPodcastMixin(object):
    def get_queryset(self):
        return NewsPodcast.objects.published()


class NewsPodcastList(NewsPodcastMixin, ListView):
    def get_queryset(self):
        query = Q()
        shows = self.request.GET.getlist('show')
        categories = self.request.GET.getlist('category')
        if shows or categories:
            query = Q(show__slug__in=shows) | Q(categories__slug__in=categories)
        return super(NewsPodcastList, self).get_queryset().filter(query).distinct()

    def get_initial_data(self):
        """
        By default, no shows or categories are preselected. If any selection is
        made for any of them, set the selection.
        """
        shows = categories = []

        selected_shows = self.request.GET.getlist('show')
        if selected_shows:
            shows = NewsShow.objects.filter(slug__in=selected_shows).values_list('slug', flat=True)

        selected_categories = self.request.GET.getlist('category')
        if selected_categories:
            categories = NewsCategory.objects.filter(slug__in=selected_categories).values_list('slug', flat=True)

        return {'show': shows, 'category': categories}

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = NewsPodcastFilter(initial=self.get_initial_data())
        return super(NewsPodcastList, self).get_context_data(*args, **kwargs)


class NewsPodcastDetail(NewsPodcastMixin, DetailView):
    pass
