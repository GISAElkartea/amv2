from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .backends import UsernameOrEmailModelBackend


auth_backend = UsernameOrEmailModelBackend()


class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    """
    Replace Django's entire clean method so that instead of calling
    `authenticate()` we can call our own backend's `authenticate()` method
    without adding it to global backends
    """

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth_backend.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                # FIXME: dirty hack
                self.user_cache.backend = 'antxetamedia.auth.backends.UsernameOrEmailModelBackend'
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
