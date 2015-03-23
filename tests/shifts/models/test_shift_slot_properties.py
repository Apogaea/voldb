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
