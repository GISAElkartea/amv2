from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password',
                  'favorite_news_shows', 'favorite_radio_shows')
        write_only_fields = ('password',)

    def save_object(self, obj, **kwargs):
        obj.set_password(self.init_data['password'])
        obj.save(**kwargs)
