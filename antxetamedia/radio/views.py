from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from .models import RadioShow, RadioCategory, RadioProducer, RadioPodcast
from .forms import RadioShowFilter


class RadioShowList(ListView):
    model = RadioShow

    def get_queryset(self):
        query = Q()
        categories = self.request.GET.getlist('category')
        producers = self.request.GET.getlist('producer')
        if categories:
            query &= Q(category__slug__in=categories)
        if producers:
            query &= Q(producer__slug__in=producers)
        return super(RadioShowList, self).get_queryset().filter(query).distinct()

    def get_initial_data(self):
        categories = RadioCategory.objects.all()
        producers = RadioProducer.objects.all()
        selected_categories = self.request.GET.getlist('category')
        selected_producers = self.request.GET.getlist('producer')
        if selected_categories or selected_producers:
            categories = categories.filter(slug__in=selected_categories)
            producers = producers.filter(slug__in=selected_producers)
        return {
            'category': categories.values_list('slug', flat=True),
            'producer': producers.values_list('slug', flat=True),
        }

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = RadioShowFilter(initial=self.get_initial_data())
        return super(RadioShowList, self).get_context_data(*args, **kwargs)


class RadioShowPodcastList(ListView):
    model = RadioPodcast
    paginate_by = 25

    def dispatch(self, request, *args, **kwargs):
        self.radioshow = get_object_or_404(RadioShow, slug=self.kwargs['slug'])
        return super(RadioShowPodcastList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        kwargs['radioshow'] = self.radioshow
        return super(RadioShowPodcastList, self).get_context_data(*args, **kwargs)

    def get_queryset(self):
        return super(RadioShowPodcastList, self).get_queryset().filter(show=self.radioshow)
