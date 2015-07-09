from django.views.generic import ListView, DetailView

from .models import ProjectProducer, ProjectShow


class ProjectProducerList(ListView):
    model = ProjectProducer


class ProjectShowDetail(DetailView):
    model = ProjectShow
