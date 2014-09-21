from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

    def save_object(self, obj):
        obj.set_password(self.init_data['password'])
        obj.save()
