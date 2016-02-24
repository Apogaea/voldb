from django.utils import timezone


def test_total_shift_slots(factories):
    role = factories.RoleFactory()

    event = factories.FutureEventFactory()

    # 30 total slots
    shift_a = factories.ShiftFactory(num_slots=10, role=role)
    shift_b = factories.ShiftFactory(num_slots=10, role=role)
    shift_c = factories.ShiftFactory(num_slots=10, role=role)

    # 2 cancelled ShiftSlots
    factories.ShiftSlotFactory(shift=shift_a, cancelled_at=timezone.now())
    factories.ShiftSlotFactory(shift=shift_b, cancelled_at=timezone.now())

    # 5 filled ShiftSlots
    factories.ShiftSlotFactory(shift=shift_a)
    factories.ShiftSlotFactory(shift=shift_b)
    factories.ShiftSlotFactory(shift=shift_b)
    factories.ShiftSlotFactory(shift=shift_c)
    factories.ShiftSlotFactory(shift=shift_c)

    assert role.total_shift_slots(event) == 30
    assert role.total_filled_shift_slots(event) == 5
