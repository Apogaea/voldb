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

    class Meta:
        model = ShiftSlot
        fields = (
            'id',
            'shift',
            'volunteer',
            'is_cancelled',
        )
        read_only_fields = (
            'id',
            'shift',
            'volunteer',
        )


class ShiftSerializer(serializers.ModelSerializer):
    open_slot_count = serializers.IntegerField(read_only=True)
    filled_slot_count = serializers.IntegerField(read_only=True)
    claimed_slots = ShiftSlotSerializer(many=True, read_only=True)
    is_locked = serializers.SerializerMethodField()

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

    def get_is_locked(self, shift):
        return not shift.event.is_registration_open


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
