from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


User = get_user_model()


class UsernameOrEmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
        except ValidationError:
            kwargs = {'username': username}
        else:
            kwargs = {'email': username}

        try:
            user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            return
        else:
            if user.check_password(password):
                return user
