from tests.factories.shifts import today_at_hour


def test_non_overlapping_adjacent_shifts(factories):
    shift_a = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    shift_b = factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_non_overlapping_separated_shifts(factories):
    shift_a = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    shift_b = factories.ShiftFactory(start_time=today_at_hour(10), shift_length=3)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_intersection(factories):
    shift_a = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    shift_b = factories.ShiftFactory(start_time=today_at_hour(8), shift_length=3)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_fully_contained(factories):
    shift_a = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    shift_b = factories.ShiftFactory(start_time=today_at_hour(7), shift_length=1)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)
