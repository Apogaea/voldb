from rest_framework import serializers

from volunteer.apps.shifts.models import (
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
    open_slot_count = serializers.IntegerField(read_only=True)
    filled_slot_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Shift
        fields = (
            'id',
            'event',
            'role',
            'start_time',
            'shift_length',
            'num_slots',
            'open_slot_count',
            'filled_slot_count',
        )
