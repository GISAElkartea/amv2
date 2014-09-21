from django.conf.urls import patterns, url

from .views import UserView


urlpatterns = patterns(
    '',
    url(r'^token/', 'rest_framework_jwt.views.obtain_jwt_token', name='auth'),
    url(r'^user/', UserView.as_view(), name='user'),
)
