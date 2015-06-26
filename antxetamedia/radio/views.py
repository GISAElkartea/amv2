from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import RadioShow, RadioCategory, RadioProducer
from .forms import RadioShowFilter


class RadioShowMixin(object):
    model = RadioShow


class RadioShowList(RadioShowMixin, ListView):
    def get_queryset(self):
        query = Q()
        categories = self.request.GET.getlist('category')
        producers = self.request.GET.getlist('producer')
        if categories or producers:
            query = Q(category__slug__in=categories) | Q(producer__slug__in=producers)
        return super(RadioShowList, self).get_queryset().filter(query)

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
            'producers': producers.values_list('slug', flat=True),
        }

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = RadioShowFilter(initial=self.get_initial_data())
        return super(RadioShowList, self).get_context_data(*args, **kwargs)


class RadioShowDetail(RadioShowMixin, DetailView):
    pass
