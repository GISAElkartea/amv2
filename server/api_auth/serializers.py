from rest_framework import serializers

from .models import UserPreferences


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserPreferences
