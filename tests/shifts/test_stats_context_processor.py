import pytest

from volunteer.apps.shifts.context_processors import shift_stats


@pytest.mark.django_db
def test_with_no_slots():
    stats = shift_stats(None)
    assert stats


def test_with_a_slot(factories):
    factories.ShiftSlotFactory()
    stats = shift_stats(None)
    assert stats
