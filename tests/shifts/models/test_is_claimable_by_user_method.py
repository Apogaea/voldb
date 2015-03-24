def test_not_claimable_if_event_not_open_for_registration(factories, user):
    past_event = factories.PastEventFactory()
    # sanity
    assert not past_event.is_registration_open

    shift = factories.ShiftFactory(num_slots=3, event=past_event)
    assert not shift.is_claimable_by_user(user)

    shift.event = factories.EventFactory()
    shift.save()
    assert shift.event.is_registration_open

    assert shift.is_claimable_by_user(user)


def test_not_claimable_if_no_slots_available(factories, user):
    shift = factories.ShiftFactory(num_slots=2)
    factories.ShiftSlotFactory.create_batch(2, shift=shift)
    # sanity
    assert not shift.has_open_slots
    assert not shift.is_claimable_by_user(user)

    shift.num_slots = 3
    shift.save()

    assert shift.has_open_slots
    assert shift.is_claimable_by_user(user)


def test_not_claimable_if_already_claimed_by_user(factories, user):
    shift = factories.ShiftFactory(num_slots=2)
    slot = factories.ShiftSlotFactory(volunteer=user, shift=shift)
    # sanity
    assert shift.has_open_slots

    assert not shift.is_claimable_by_user(user)

    slot.cancel()

    assert shift.has_open_slots
    assert shift.is_claimable_by_user(user)
