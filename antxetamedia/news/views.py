from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import NewsPodcast, NewsShow, NewsCategory
from .forms import NewsPodcastFilter


class NewsPodcastMixin(object):
    def get_queryset(self):
        return NewsPodcast.objects.published()


class NewsPodcastList(NewsPodcastMixin, ListView):
    def get_queryset(self):
        shows = self.request.GET.getlist('show')
        categories = self.request.GET.getlist('category')
        query = Q(show__slug__in=shows) & Q(categories__slug__in=categories)
        return super(NewsPodcastList, self).get_queryset().filter(query)

    def get_initial_shows(self):
        qs = NewsShow.objects.all()
        selected = self.request.GET.getlist('show')
        qs = qs.filter(slug__in=selected) if selected else qs
        return qs.values_list('slug', flat=True)

    def get_initial_categories(self):
        qs = NewsCategory.objects.all()
        selected = self.request.GET.getlist('category')
        qs = qs.filter(slug__in=selected) if selected else qs
        return qs.values_list('slug', flat=True)

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = NewsPodcastFilter(initial={
            'show': self.get_initial_shows(),
            'category': self.get_initial_categories(),
        })
        return super(NewsPodcastList, self).get_context_data(*args, **kwargs)


class NewsPodcastDetail(NewsPodcastMixin, DetailView):
    pass
