from django.conf.urls import url

from .views import WelcomePage, FrontPage

urlpatterns = [
    url(r'^$', FrontPage.as_view(), name='frontpage'),
    url(r'^welcome/$', WelcomePage.as_view(), name='welcomepage'),
]
