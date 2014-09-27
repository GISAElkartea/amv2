from django.conf.urls import patterns, url

from .views import UserView, ConfirmationView


urlpatterns = patterns(
    '',
    url(r'^token/', 'rest_framework_jwt.views.obtain_jwt_token', name='auth'),
    url(r'^user/', UserView.as_view(), name='user'),
    url(r'^reset/', ConfirmationView.as_view(), name='password_reset'),
)
