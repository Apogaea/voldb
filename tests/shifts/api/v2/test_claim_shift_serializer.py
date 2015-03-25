import pytest

from volunteer.apps.shifts.api.v2.serializers import (
    ClaimShiftSerializer,
)


def test_non_passcode_shift_serialization_no_code(factories):
    shift = factories.ShiftFactory()
    serializer = ClaimShiftSerializer(shift, data={})
    assert serializer.is_valid()


def test_non_passcode_shift_serialization_with_code(factories):
    shift = factories.ShiftFactory()
    serializer = ClaimShiftSerializer(shift, data={'unlock_code': 'a code'})
    assert serializer.is_valid()


def test_passcoded_shift_serialization_without_code(factories):
    shift = factories.ShiftFactory(code='test-code')
    serializer = ClaimShiftSerializer(shift, data={})
    assert not serializer.is_valid()


def test_passcoded_shift_serialization_with_wrong_code(factories):
    shift = factories.ShiftFactory(code='test-code')
    serializer = ClaimShiftSerializer(shift, data={'unlock_code': 'wrong-code'})
    assert not serializer.is_valid()


@pytest.mark.parametrize(
    'code', ['test-code', 'Test-Code', 'TEST-CODE'],
)
def test_passcoded_shift_serialization_with_correct_codes(factories, code):
    shift = factories.ShiftFactory(code='test-code')
    serializer = ClaimShiftSerializer(shift, data={'unlock_code': code})
    assert serializer.is_valid()
