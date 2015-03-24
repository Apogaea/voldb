def test_cancelled_shifts_are_not_included(factories, user):
    shift_a = factories.ShiftFactory()
    factories.ShiftSlotFactory(volunteer=user, shift=shift_a)

    shift_b = factories.ShiftFactory()
    factories.CancelledShiftSlotFactory(volunteer=user, shift=shift_b)

    shift_c = factories.ShiftFactory()
    factories.ShiftSlotFactory(volunteer=user, shift=shift_c)

    assert len(user.shifts) == 2
    assert shift_a in user.shifts
    assert shift_b not in user.shifts
    assert shift_c in user.shifts
