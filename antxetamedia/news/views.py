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
        shows = NewsShow.objects.all()
        categories = NewsCategory.objects.all()
        selected_shows = self.request.GET.getlist('show')
        selected_categories = self.request.GET.getlist('category')
        if selected_shows or selected_categories:
            shows = shows.filter(slug__in=selected_shows)
            categories = categories.filter(slug__in=selected_categories)
        return {
            'show': shows.values_list('slug', flat=True),
            'category': categories.values_list('slug', flat=True),
        }

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = NewsPodcastFilter(initial=self.get_initial_data())
        return super(NewsPodcastList, self).get_context_data(*args, **kwargs)


class NewsPodcastDetail(NewsPodcastMixin, DetailView):
    pass
