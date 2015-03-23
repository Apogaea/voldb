from volunteer.apps.shifts.api.v2.serializers import (
    ShiftSerializer,
)


def test_shift_serialization(factories):
    shift = factories.ShiftFactory()
    serializer = ShiftSerializer(shift)

    data = serializer.data
    assert data['id'] == shift.pk
