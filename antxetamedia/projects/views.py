from django.views.generic import ListView, DetailView

from .models import ProjectShow


class ProjectShowMixin(object):
    queryset = ProjectShow.objects.order_by('-creation_date')


class ProjectShowList(ProjectShowMixin, ListView):
    paginate_by = 20


class ProjectShowDetail(ProjectShowMixin, DetailView):
    pass
