from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from antxetamedia.news.models import NewsPodcast
from antxetamedia.radio.models import RadioPodcast
from antxetamedia.events.models import Event
from antxetamedia.widgets.models import Widget


VISITED_COOKIE = 'welcome_page'
VISITED_COOKIE_VALUE = 'visited'


class WelcomePage(TemplateView):
    template_name = 'welcome.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Set a cookie whenever a user visits this page.
        """
        response = super(WelcomePage, self).dispatch(request, *args, **kwargs)
        response.set_cookie(VISITED_COOKIE, VISITED_COOKIE_VALUE)
        return response


class FrontPage(TemplateView):
    template_name = 'frontpage.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect to the welcome page if the user isn't authenticated and it's their first visit.
        """
        if not request.user.is_authenticated() and request.COOKIES.get(VISITED_COOKIE, None) != VISITED_COOKIE_VALUE:
            return HttpResponseRedirect(reverse('welcomepage'))
        return super(FrontPage, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        kwargs['newspodcast_list'] = NewsPodcast.objects.all()
        kwargs['radiopodcast_list'] = RadioPodcast.objects.all()
        kwargs['event_list'] = Event.objects.all()
        kwargs['widget_list'] = Widget.objects.all()
        return super(FrontPage, self).get_context_data(*args, **kwargs)
