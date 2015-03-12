from tests.factories.shifts import (
    today_at_hour,
)


def test_doesnt_span_midnight(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    assert not shift.is_midnight_spanning


def test_does_span_midnight(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(23), shift_length=3)
    assert shift.is_midnight_spanning


def test_really_long_shift(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(23), shift_length=26)
    assert shift.is_midnight_spanning


def test_ends_at_midnight(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(21), shift_length=3)
    assert not shift.is_midnight_spanning
