from django.views.generic import DetailView

from .models import Flatpage


class FlatpageDetail(DetailView):
    model = Flatpage
    slug_field = 'path'
