from django.utils import timezone


def test_has_open_slots(factories):
    shift = factories.ShiftFactory(num_slots=2)

    assert shift.has_open_slots
    slot = factories.ShiftSlotFactory(shift=shift)
    assert shift.has_open_slots
    factories.ShiftSlotFactory(shift=shift)
    assert not shift.has_open_slots
    slot.cancel()
    assert shift.has_open_slots
    factories.ShiftSlotFactory(shift=shift)
    assert not shift.has_open_slots
    factories.ShiftSlotFactory(shift=shift)
    assert not shift.has_open_slots


def test_is_cancelled_getting(factories):
    slot = factories.ShiftSlotFactory()

    assert not slot.is_cancelled
    slot.cancelled_at = timezone.now()
    assert slot.is_cancelled


def test_is_cancelled_setting(factories):
    slot = factories.ShiftSlotFactory()

    slot.cancelled_at = timezone.now()

    when = slot.cancelled_at
    slot.is_cancelled = True
    assert slot.cancelled_at == when
    slot.is_cancelled = False
    assert slot.cancelled_at is None
