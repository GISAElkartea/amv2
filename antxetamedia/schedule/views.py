from django.views.generic import ListView

from .models import Broadcast


class BroadcastList(ListView):
    model = Broadcast
