from volunteer.apps.shifts.api.v2.serializers import (
    ShiftSlotSerializer,
)


def test_shift_serialization(factories):
    slot = factories.ShiftSlotFactory()
    serializer = ShiftSlotSerializer(slot)

    data = serializer.data
    assert data['id'] == slot.pk
