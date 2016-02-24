from django.utils import timezone


def test_total_shift_slots(factories):
    dept = factories.DepartmentFactory()

    role_a = factories.RoleFactory(department=dept)
    role_b = factories.RoleFactory(department=dept)

    # 30 total slots
    shift_a = factories.ShiftFactory(num_slots=10, role=role_a)
    shift_b = factories.ShiftFactory(num_slots=10, role=role_b)
    shift_c = factories.ShiftFactory(num_slots=10, role=role_b)

    # 2 cancelled ShiftSlots
    factories.ShiftSlotFactory(shift=shift_a, cancelled_at=timezone.now())
    factories.ShiftSlotFactory(shift=shift_b, cancelled_at=timezone.now())

    # 5 filled ShiftSlots
    factories.ShiftSlotFactory(shift=shift_a)
    factories.ShiftSlotFactory(shift=shift_b)
    factories.ShiftSlotFactory(shift=shift_b)
    factories.ShiftSlotFactory(shift=shift_c)
    factories.ShiftSlotFactory(shift=shift_c)

    assert dept.total_shift_slots(None) == 30
    assert dept.total_filled_shift_slots(None) == 5
