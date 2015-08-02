import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView, TemplateView, FormView

from antxetamedia.news.models import NewsPodcast, NewsCategory
from antxetamedia.radio.models import RadioPodcast, RadioShow
from antxetamedia.events.models import Event
from antxetamedia.widgets.models import Widget

from .forms import ConfigureFrontPageForm


class FrontPage(TemplateView):
    template_name = 'frontpage/frontpage.html'

    def get_context_data(self, *args, **kwargs):
        NEWSPODCASTS = getattr(settings, 'FRONTPAGE_NEWSPODCASTS', 10)
        RADIOPODCASTS = getattr(settings, 'FRONTPAGE_RADIOPODCASTS', 5)
        EVENTS = getattr(settings, 'FRONTPAGE_EVENTS', 5)
        kwargs['newspodcast_list'] = NewsPodcast.objects.favourites(self.request)[:NEWSPODCASTS]
        kwargs['radiopodcast_list'] = RadioPodcast.objects.favourites(self.request)[:RADIOPODCASTS]
        kwargs['event_list'] = Event.objects.upcoming(count=EVENTS)
        kwargs['widget_list'] = Widget.objects.all()
        return super(FrontPage, self).get_context_data(*args, **kwargs)


class ConfigureFrontPage(FormView):
    form_class = ConfigureFrontPageForm
    template_name = 'frontpage/configure.html'
    cookies = {}

    def get_initial(self):
        newscategories = self.request.COOKIES.get(settings.NEWSCATEGORIES_COOKIE)
        if newscategories:
            newscategories = json.loads(newscategories)
        else:
            newscategories = NewsCategory.objects.values_list('pk', flat=True)

        radioshows = self.request.COOKIES.get(settings.RADIOSHOWS_COOKIE)
        if radioshows:
            radioshows = json.loads(radioshows)
        else:
            radioshows = RadioShow.objects.values_list('pk', flat=True)

        return {'newscategories': newscategories, 'radioshows': radioshows}

    def form_valid(self, form):
        newscategories = list(form.cleaned_data['newscategories'].values_list('pk', flat=True))
        self.cookies[settings.NEWSCATEGORIES_COOKIE] = json.dumps(newscategories)
        radioshows = list(form.cleaned_data['radioshows'].values_list('pk', flat=True))
        self.cookies[settings.RADIOSHOWS_COOKIE] = json.dumps(radioshows)
        return super(ConfigureFrontPage, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        kwargs['NEWSCATEGORIES_COOKIE'] = settings.NEWSCATEGORIES_COOKIE
        kwargs['RADIOSHOWS_COOKIE'] = settings.RADIOSHOWS_COOKIE
        return super(ConfigureFrontPage, self).get_context_data(*args, **kwargs)

    def get_success_url(self):
        return reverse('frontpage')

    def dispatch(self, request, *args, **kwargs):
        response = super(ConfigureFrontPage, self).dispatch(request, *args, **kwargs)
        for key, value in self.cookies.items():
            response.set_cookie(key, value)
        return response


class ResetFrontPageConfiguration(RedirectView):
    permanent = False

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('frontpage')

    def dispatch(self, request, *args, **kwargs):
        response = super(ResetFrontPageConfiguration, self).dispatch(request, *args, **kwargs)
        response.delete_cookie(settings.NEWSCATEGORIES_COOKIE)
        response.delete_cookie(settings.RADIOSHOWS_COOKIE)
        return response
