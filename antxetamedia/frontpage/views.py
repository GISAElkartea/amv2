from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class WelcomePage(TemplateView):
    template_name = 'welcome.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Set a cookie whenever a user visits this page.
        """
        response = super(WelcomePage, self).dispatch(request, *args, **kwargs)
        response.set_cookie('welcome_page', 'visited')
        return response


class FrontPage(TemplateView):
    template_name = 'frontpage.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect to the welcome page if the user isn't authenticated and it's their first visit.
        """
        if not request.user.is_authenticated() and request.COOKIES.get('welcome_page', None) != 'visited':
            return HttpResponseRedirect(reverse('welcomepage'))
        return super(FrontPage, self).dispatch(request, *args, **kwargs)
