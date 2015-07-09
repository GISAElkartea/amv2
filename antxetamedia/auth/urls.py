from django.conf.urls import include, url

from .forms import UsernameOrEmailAuthenticationForm

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'authentication_form': UsernameOrEmailAuthenticationForm}, name='login'),
    url(r'^', include('registration.backends.default.urls')),
]
