from django.views.generic import TemplateView


class Frontpage(TemplateView):
    template_name = 'base.html'
