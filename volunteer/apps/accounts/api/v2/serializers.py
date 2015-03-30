from rest_framework import serializers

from volunteer.apps.accounts.models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    shifts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'display_name',
            'is_anonymous',
            'is_authenticated',
            'shifts',
        )

    def get_display_name(self, user):
        if user.is_anonymous():
            return None
        return user.profile.display_name

    def get_shifts(self, user):
        if user.is_anonymous():
            return []
        return [s.pk for s in user.shifts]
