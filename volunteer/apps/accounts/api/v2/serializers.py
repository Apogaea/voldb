from rest_framework import serializers

from volunteer.apps.accounts.models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name')

    class Meta:
        model = User
        fields = (
            'id',
            'display_name',
        )
