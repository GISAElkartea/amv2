from rest_framework import serializers

from .models import APIUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = APIUser
