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


def test_filtered_to_only_current_event_shifts(settings, factories, user, models):
    past_event = factories.PastEventFactory()
    past_shift = factories.ShiftFactory(event=past_event)
    factories.ShiftSlotFactory(volunteer=user, shift=past_shift)

    # Current stuff
    current_event = factories.FutureEventFactory()

    settings.CURRENT_EVENT_ID = current_event.pk

    shift_a = factories.ShiftFactory()
    # sanity check
    assert shift_a.event == current_event

    factories.ShiftSlotFactory(volunteer=user, shift=shift_a)

    shift_b = factories.ShiftFactory()
    factories.CancelledShiftSlotFactory(volunteer=user, shift=shift_b)

    shift_c = factories.ShiftFactory()
    factories.ShiftSlotFactory(volunteer=user, shift=shift_c)

    assert len(user.shifts) == 2
    assert shift_a in user.shifts
    assert shift_b not in user.shifts
    assert shift_c in user.shifts
    assert past_shift not in user.shifts
