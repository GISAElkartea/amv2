import json

from django.core.urlresolvers import reverse
from django.views.generic import RedirectView, TemplateView, FormView

from antxetamedia.news.models import NewsPodcast, NewsCategory
from antxetamedia.radio.models import RadioPodcast, RadioShow
from antxetamedia.events.models import Event
from antxetamedia.widgets.models import Widget

from .forms import ConfigureFrontPageForm


NEWSCATEGORIES_COOKIE = 'newscategories'
RADIOSHOWS_COOKIE = 'radioshows'


class FrontPage(TemplateView):
    template_name = 'frontpage/frontpage.html'

    def get_newspodcasts(self):
        qs = NewsPodcast.objects.published()
        newscategories = self.request.COOKIES.get(NEWSCATEGORIES_COOKIE)
        if newscategories:
            newscategories = json.loads(newscategories)
            qs = qs.filter(categories__pk__in=newscategories)
        return qs

    def get_radiopodcasts(self):
        qs = RadioPodcast.objects.published()
        radioshows = self.request.COOKIES.get(RADIOSHOWS_COOKIE)
        if radioshows:
            radioshows = json.loads(radioshows)
            qs = qs.filter(show__pk__in=radioshows)
        return qs

    def get_context_data(self, *args, **kwargs):
        kwargs['newspodcast_list'] = self.get_newspodcasts()
        kwargs['radiopodcast_list'] = self.get_radiopodcasts()
        kwargs['event_list'] = Event.objects.all()
        kwargs['widget_list'] = Widget.objects.all()
        return super(FrontPage, self).get_context_data(*args, **kwargs)


class ConfigureFrontPage(FormView):
    form_class = ConfigureFrontPageForm
    template_name = 'frontpage/configure.html'
    cookies = {}

    def get_initial(self):
        newscategories = self.request.COOKIES.get(NEWSCATEGORIES_COOKIE)
        if newscategories:
            newscategories = json.loads(newscategories)
        else:
            newscategories = NewsCategory.objects.values_list('pk', flat=True)

        radioshows = self.request.COOKIES.get(RADIOSHOWS_COOKIE)
        if radioshows:
            radioshows = json.loads(radioshows)
        else:
            radioshows = RadioShow.objects.values_list('pk', flat=True)

        return {'newscategories': newscategories, 'radioshows': radioshows}

    def form_valid(self, form):
        newscategories = list(form.cleaned_data['newscategories'].values_list('pk', flat=True))
        self.cookies[NEWSCATEGORIES_COOKIE] = json.dumps(newscategories)
        radioshows = list(form.cleaned_data['radioshows'].values_list('pk', flat=True))
        self.cookies[RADIOSHOWS_COOKIE] = json.dumps(radioshows)
        return super(ConfigureFrontPage, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        kwargs['NEWSCATEGORIES_COOKIE'] = NEWSCATEGORIES_COOKIE
        kwargs['RADIOSHOWS_COOKIE'] = RADIOSHOWS_COOKIE
        return super(ConfigureFrontPage, self).get_context_data(*args, **kwargs)

    def get_success_url(self):
        return reverse('frontpage')

    def dispatch(self, request, *args, **kwargs):
        response = super(ConfigureFrontPage, self).dispatch(request, *args, **kwargs)
        for key, value in self.cookies.items():
            response.set_cookie(key, value)
        return response


class ResetFrontPageConfiguration(RedirectView):
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('frontpage')

    def dispatch(self, request, *args, **kwargs):
        response = super(ResetFrontPageConfiguration, self).dispatch(request, *args, **kwargs)
        response.delete_cookie(NEWSCATEGORIES_COOKIE)
        response.delete_cookie(RADIOSHOWS_COOKIE)
        return response
