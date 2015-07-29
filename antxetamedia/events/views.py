from django.views.generic import ListView, DetailView

from .models import Event


class EventMixin(object):
    model = Event


class EventList(EventMixin, ListView):
    template_name = 'events/event_list.html'
    context_object_name = 'event_list'
    paginate_by = 10

    def get_queryset(self):
        # NOTE: Little hack, event generator can be infinite, limit it to 10 pages
        return list(Event.objects.upcoming(self.paginate_by * 10))


class EventDetail(EventMixin, DetailView):
    pass
