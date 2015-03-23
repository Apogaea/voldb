from rest_framework import serializers

from volunteer.apps.departments.api.v2.serializers import (
    DepartmentSerializer,
)

from volunteer.apps.shifts.models import (
    Role,
    Shift,
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


class RoleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    shifts = ShiftSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'department',
            'name',
            'description',
            'shifts',
        )
