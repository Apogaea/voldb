from rest_framework import serializers

from volunteer.apps.departments.api.v2.serializers import (
    DepartmentSerializer,
)

from volunteer.apps.shifts.models import (
    Role,
    Shift,
    ShiftSlot,
)


class ShiftSlotSerializer(serializers.ModelSerializer):
    is_cancelled = serializers.BooleanField()
    volunteer_display_name = serializers.CharField(source='volunteer.profile.display_name')

    class Meta:
        model = ShiftSlot
        fields = (
            'id',
            'shift',
            'volunteer',
            'volunteer_display_name',
            'is_cancelled',
        )
        read_only_fields = (
            'id',
            'shift',
            'volunteer',
            'volunteer_display_name',
        )


class ShiftSerializer(serializers.ModelSerializer):
    open_slot_count = serializers.IntegerField(read_only=True)
    filled_slot_count = serializers.IntegerField(read_only=True)
    claimed_slots = ShiftSlotSerializer(many=True, read_only=True)
    is_locked = serializers.ReadOnlyField()

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
            'claimed_slots',
            'is_locked',
        )


class RoleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'department',
            'name',
            'description',
        )
