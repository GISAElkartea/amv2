from django.conf.urls import patterns, url

from .views import AuthView, UserView


urlpatterns = patterns(
    '',
    url(r'^auth/', AuthView.as_view(), name='auth'),
    url(r'^user/', UserView.as_view(), name='user'),
)
