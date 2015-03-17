from rest_framework import serializers

from shifts.models import (
    Role,
    Shift,
)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'department',
            'name',
            'description',
        )


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = (
            'id',
            'role',
            'start_time',
            'shift_length',
            'owner',
        )