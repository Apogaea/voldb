from django.utils.crypto import (
    constant_time_compare,
)
from rest_framework import serializers

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)


class ShiftSlotSerializer(serializers.ModelSerializer):
    is_cancelled = serializers.BooleanField()
    volunteer_display_name = serializers.ReadOnlyField(source='volunteer.profile.display_name')

    class Meta:
        model = ShiftSlot
        fields = (
            'id',
            'shift',
            'volunteer',
            'volunteer_display_name',
            'is_cancelled',
            'is_locked',
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
            'shift_minutes',
            'num_slots',
            'open_slot_count',
            'filled_slot_count',
            'claimed_slots',
            'is_locked',
            'is_protected',
        )


class ClaimShiftSerializer(serializers.ModelSerializer):
    unlock_code = serializers.CharField(required=False)

    class Meta:
        model = Shift
        fields = (
            'unlock_code',
        )

    def validate(self, data):
        if self.instance.code:
            unlock_code = data.get('unlock_code')
            if unlock_code:
                if constant_time_compare(unlock_code.lower(), self.instance.code.lower()):
                    return data
            raise serializers.ValidationError("Invalid Unlock Code")
        return data
