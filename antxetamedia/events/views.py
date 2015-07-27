from django.views.generic import ListView, DetailView

from .models import Event


class EventMixin(object):
    model = Event


class EventList(EventMixin, ListView):
    template_name = 'events/event_list.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.upcoming()


class EventDetail(EventMixin, DetailView):
    pass
