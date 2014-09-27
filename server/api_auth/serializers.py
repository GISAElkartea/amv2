from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'favorite_radio_shows', 'favorite_news_shows')

    def save_object(self, obj, **kwargs):
        obj.set_password(self.init_data['password'])
        obj.save(**kwargs)
