from django.conf.urls import url

from .views import WelcomePage, FrontPage, ConfigureFrontPage, ResetFrontPageConfiguration

urlpatterns = [
    url(r'^$', FrontPage.as_view(), name='frontpage'),
    url(r'^configure/$', ConfigureFrontPage.as_view(), name='configure-frontpage'),
    url(r'^configure/reset$', ResetFrontPageConfiguration.as_view(), name='reset-frontpage-configuration'),
    url(r'^welcome/$', WelcomePage.as_view(), name='welcomepage'),
]
