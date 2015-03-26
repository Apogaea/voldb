import pytest

import datetime

from django.utils import timezone

from volunteer.apps.shifts.models import Shift
from volunteer.apps.shifts.utils import (
    pairwise,
    shifts_to_tabular_data,
    get_num_columns,
    shifts_as_grid,
    collapse_empty_columns,
    build_empty_column,
    build_shift_column,
    check_if_overlap,
    check_if_midnight_spanning,
    shifts_to_non_overlapping_rows,
)
from tests.factories.shifts import (
    today_at_hour,
    yesterday_at_hour,
    tomorrow_at_hour,
)


def ShiftDict(*args, **kwargs):
    return shift_to_dict(Shift(*args, **kwargs))


def shift_to_dict(shift):
    return {
        'id': shift.pk,
        'role_id': shift.role_id,
        'start_time': shift.start_time.astimezone(timezone.get_default_timezone()),
        'shift_minutes': shift.shift_minutes,
        'end_time': shift.end_time.astimezone(timezone.get_default_timezone()),
        'is_empty': False,
        'columns': shift.shift_minutes,
        'open_slot_count': shift.open_slot_count,
    }


def _wrap_in_lists(items):
    return [[item] for item in items]


HOUR = 60
ONE_DAY = HOUR * 24


#
# check_if_overlap tests
#
def test_non_overlapping_adjacent_shifts():
    shift_a = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    shift_b = ShiftDict(start_time=today_at_hour(9), shift_minutes=3 * HOUR)

    assert not check_if_overlap(shift_a, shift_b)
    assert not check_if_overlap(shift_b, shift_a)


def test_non_overlapping_separated_shifts():
    shift_a = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    shift_b = ShiftDict(start_time=today_at_hour(10), shift_minutes=3 * HOUR)

    assert not check_if_overlap(shift_a, shift_b)
    assert not check_if_overlap(shift_b, shift_a)


def test_intersection():
    shift_a = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    shift_b = ShiftDict(start_time=today_at_hour(8), shift_minutes=3 * HOUR)

    assert check_if_overlap(shift_a, shift_b)
    assert check_if_overlap(shift_b, shift_a)


def test_fully_contained():
    shift_a = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    shift_b = ShiftDict(start_time=today_at_hour(7), shift_minutes=1 * HOUR)

    assert check_if_overlap(shift_a, shift_b)
    assert check_if_overlap(shift_b, shift_a)


#
# check_if_midnight_spanning tests for correct column sizes
#
def test_non_midnight_spanning_shift():
    shift = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    assert not check_if_midnight_spanning(shift)
    column_data = build_shift_column([shift], datetime.date.today())
    assert column_data.get('columns') == shift['shift_minutes']


def test_span_previous_midnight():
    shift = ShiftDict(start_time=yesterday_at_hour(23), shift_minutes=9 * HOUR)
    assert check_if_midnight_spanning(shift)
    column_data = build_shift_column([shift], datetime.date.today())
    assert column_data.get('columns') == 8 * HOUR


def test_span_next_midnight():
    shift = ShiftDict(start_time=today_at_hour(23), shift_minutes=9 * HOUR)
    assert check_if_midnight_spanning(shift)
    column_data = build_shift_column([shift], datetime.date.today())
    assert column_data.get('columns') == 1 * HOUR


def test_doesnt_span_midnight():
    shift = ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    assert not check_if_midnight_spanning(shift)


def test_does_span_midnight():
    shift = ShiftDict(start_time=today_at_hour(23), shift_minutes=3 * HOUR)
    assert check_if_midnight_spanning(shift)


def test_really_long_shift():
    shift = ShiftDict(start_time=today_at_hour(23), shift_minutes=26 * HOUR)
    assert check_if_midnight_spanning(shift)


def test_ends_at_midnight():
    shift = ShiftDict(start_time=today_at_hour(21), shift_minutes=3 * HOUR)
    assert not check_if_midnight_spanning(shift)


#
# shifts_to_non_overlapping_rows tests
#
def has_overlaps(shifts):
    _shifts = zip(*shifts)[0]
    return any(check_if_overlap(l, r) for l, r in pairwise(_shifts))


def test_has_overlaps_util():
    assert not has_overlaps((
        [ShiftDict(start_time=today_at_hour(0), shift_minutes=3 * HOUR)],
        [ShiftDict(start_time=today_at_hour(3), shift_minutes=3 * HOUR)],
        [ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR)],
    ))
    assert has_overlaps((
        [ShiftDict(start_time=today_at_hour(0), shift_minutes=3 * HOUR)],
        [ShiftDict(start_time=today_at_hour(2), shift_minutes=3 * HOUR)],
    ))


def test_with_no_overlaps():
    shifts = (
        ShiftDict(start_time=today_at_hour(0), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(3), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(9), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(12), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(15), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(21), shift_minutes=3 * HOUR),
    )
    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 1
    assert len(rows[0]) == 8
    # any?
    assert not any(
        has_overlaps(row) for row in rows
    )


def test_single_set_of_overlaps():
    shifts = (
        # modulo 0
        ShiftDict(start_time=today_at_hour(0), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(3), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(9), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(12), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(15), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(21), shift_minutes=3 * HOUR),
        # modulo 1
        ShiftDict(start_time=today_at_hour(1), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(4), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(7), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(10), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(13), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(16), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(19), shift_minutes=3 * HOUR),
    )

    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 2
    assert len(rows[0]) == 8
    assert len(rows[1]) == 7
    # any?
    assert not any(
        has_overlaps(row) for row in rows
    )


def test_two_sets_of_overlap():
    shifts = (
        # modulo 0
        ShiftDict(start_time=today_at_hour(0), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(3), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(9), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(12), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(15), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(21), shift_minutes=3 * HOUR),
        # modulo 1
        ShiftDict(start_time=today_at_hour(1), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(4), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(7), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(10), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(13), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(16), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(19), shift_minutes=3 * HOUR),
        # modulo 2
        ShiftDict(start_time=today_at_hour(2), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(5), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(8), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(11), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(14), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(17), shift_minutes=3 * HOUR),
        ShiftDict(start_time=today_at_hour(20), shift_minutes=3 * HOUR),
    )
    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 3
    assert len(rows[0]) == 8
    assert len(rows[1]) == 7
    assert len(rows[2]) == 7
    # any?
    assert not all(
        has_overlaps(row) for row in rows
    )


def assert_columns_all_at_correct_location(data):
    for index, column in enumerate(data):
        if column['open_on_left']:
            continue
        assert get_num_columns(data[:index]) == column['start_time'].hour * HOUR + column['start_time'].minute


#
# shifts_to_tabular_data tests
#
def test_with_no_shifts():
    data = shifts_to_tabular_data([], datetime.date.today())
    assert len(data) == ONE_DAY

    assert all(list(d['shifts'] == [] for d in data))
    assert get_num_columns(data) == ONE_DAY

    assert_columns_all_at_correct_location(data)


def test_with_non_overlapping():
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                      [*-*-*]
                            [*-*-*]
                                        [*-*-*]
    """
    shifts = []
    # shift from 9am to noon
    shifts.append(ShiftDict(start_time=today_at_hour(9), shift_minutes=3 * HOUR))
    # shift from noon to 3pm
    shifts.append(ShiftDict(start_time=today_at_hour(12), shift_minutes=3 * HOUR))
    # shift from 6pm to 9pm
    shifts.append(ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR))

    data = shifts_to_tabular_data(_wrap_in_lists(shifts), datetime.date.today())
    assert get_num_columns(data) == ONE_DAY

    assert_columns_all_at_correct_location(data)

    collapsed_data = collapse_empty_columns(data)

    empties = collapsed_data[0], collapsed_data[3], collapsed_data[5]

    assert all(list(d['shifts'] == [] for d in empties))

    non_empties = collapsed_data[1], collapsed_data[2], collapsed_data[4]

    assert all(list(d['columns'] == 3 * HOUR for d in non_empties))


def test_with_simultaneous_shifts():
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                                        [*-*-*]
                                        [*-*-*]
    """
    shifts = []
    # shift from 6pm to 9pm
    shifts.append(ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(18), shift_minutes=3 * HOUR))

    with pytest.raises(ValueError):
        shifts_to_tabular_data(_wrap_in_lists(shifts), datetime.date.today())


def test_with_overlapping_shifts():
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                [*-*-*]
                    [*-*-*]
                        [*-*-*]
    """
    shifts = []
    # 3 hour shifts, staggered 2 hours apart.
    shifts.append(ShiftDict(start_time=today_at_hour(6), shift_minutes=3 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(8), shift_minutes=3 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(10), shift_minutes=3 * HOUR))

    with pytest.raises(ValueError):
        shifts_to_tabular_data(_wrap_in_lists(shifts), datetime.date.today())


def test_with_shift_that_spans_previous_midnight():
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
    *-*-*-**]
            [*-*-*-*-*]
                      [*-*-*-*-*]
                                [*-*-*-*-*]
    """
    shifts = []
    # 3 hour shifts, staggered 2 hours apart.
    shifts.append(ShiftDict(start_time=yesterday_at_hour(23), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(4), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(9), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(14), shift_minutes=5 * HOUR))

    data = shifts_to_tabular_data(_wrap_in_lists(shifts), datetime.date.today())
    assert get_num_columns(data) == ONE_DAY

    assert_columns_all_at_correct_location(data)

    assert len(data) == 5 * HOUR + 4
    assert data[0]['columns'] == 4 * HOUR
    assert all(list(c['columns'] == 5 * HOUR for c in data[1:4]))
    assert all(list(c['columns'] == 1 for c in data[4:]))


def test_with_shift_that_spans_upcoming_midnight():
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
              [*-*-*-*-*]
                        [*-*-*-*-*]
                                  [*-*-*-*-*]
                                            [*-*-*-*-
    """
    shifts = []
    # 3 hour shifts, staggered 2 hours apart.
    shifts.append(ShiftDict(start_time=today_at_hour(5), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(10), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(15), shift_minutes=5 * HOUR))
    shifts.append(ShiftDict(start_time=today_at_hour(20), shift_minutes=5 * HOUR))

    data = shifts_to_tabular_data(_wrap_in_lists(shifts), datetime.date.today())

    assert get_num_columns(data) == ONE_DAY

    assert_columns_all_at_correct_location(data)

    assert len(data) == 5 * HOUR + 4
    assert all(c['columns'] == 1 for c in data[:5 * HOUR])
    assert all(c['columns'] == 5 * HOUR for c in data[5 * HOUR:5 * HOUR + 3])
    assert data[-1]['columns'] == 4 * HOUR


#
# shifts_as_grid tests
#
@pytest.mark.django_db
def test_grouping(factories):
    today = today_at_hour(0).date()
    yesterday = yesterday_at_hour(0).date()

    # shift yesterday dpw
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                            [*-*-*]
                                  [*-*-*]
    """
    factories.ShiftFactory(start_time=yesterday_at_hour(12), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=yesterday_at_hour(15), shift_minutes=3 * HOUR)
    # shift today dpw
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                [*-*-*]
                [*-*-*]
                      [*-*-*]
                      [*-*-*]
                            [*-*-*]
                            [*-*-*]
                                  [*-*-*]
                                  [*-*-*]
    """
    factories.ShiftFactory(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(6), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(9), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(9), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(12), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(12), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(15), shift_minutes=3 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(15), shift_minutes=3 * HOUR)
    # shift today dpw
    """
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                      [*-*-*-*-*-*]
                                  [*-*-*-*-*-*]
    """
    factories.ShiftFactory(start_time=today_at_hour(9), shift_minutes=6 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(15), shift_minutes=6 * HOUR)

    data = list(shifts_as_grid(Shift.objects.all()))

    # grouped by date and length
    # -: (yesterday, length-3)
    # -: (today, length-3)
    # -: (today, length-6)
    assert len(data) == 3

    data_0, data_1, data_2 = data

    assert data_0['date'] == yesterday
    assert data_0['length'] == 3 * HOUR
    assert len(data_0['cells']) == 4  # this is the tabular data, dunno what to assert.

    assert data_1['date'] == today
    assert data_1['length'] == 3 * HOUR
    assert len(data_1['cells']) == 6  # this is the tabular data, dunno what to assert.

    assert data_2['date'] == today
    assert data_2['length'] == 6 * HOUR
    assert len(data_2['cells']) == 4  # this is the tabular data, dunno what to assert.


@pytest.mark.django_db
def test_complex_grouping_with_shifts_spanning_midnight(factories):
    """
    Yesterday
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                          [*-*-*-*-*-*-*-*-*-*-*-*]
                                                  [*-
    Today
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
    -*-*-*-*-*-*-*-*-*-*-*]
                          [*-*-*-*-*-*-*-*-*-*-*-*]
                                                  [*-
    Tomorrow
    0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
    -*-*-*-*-*-*-*-*-*-*-*]
                          [*-*-*-*-*-*-*-*-*-*]
    """
    today = today_at_hour(0).date()
    yesterday = yesterday_at_hour(0).date()
    tomorrow = tomorrow_at_hour(0).date()

    # shift yesterday dpw
    factories.ShiftFactory(start_time=yesterday_at_hour(11), shift_minutes=12 * HOUR)
    factories.ShiftFactory(start_time=yesterday_at_hour(23), shift_minutes=12 * HOUR)
    # shift today dpw
    factories.ShiftFactory(start_time=today_at_hour(11), shift_minutes=12 * HOUR)
    factories.ShiftFactory(start_time=today_at_hour(23), shift_minutes=12 * HOUR)
    # shift tomorrow dpw
    factories.ShiftFactory(start_time=tomorrow_at_hour(11), shift_minutes=12 * HOUR)

    data = list(shifts_as_grid(Shift.objects.all()))

    assert len(data) == 3

    data_0, data_1, data_2 = data

    assert data_0['date'] == yesterday
    assert len(data_0['cells']) == 2  # this is the tabular data, dunno what to assert.

    assert data_1['date'] == today
    assert len(data_1['cells']) == 2  # this is the tabular data, dunno what to assert.

    assert data_2['date'] == tomorrow
    assert len(data_2['cells']) == 2  # this is the tabular data, dunno what to assert.


@pytest.mark.django_db
def test_shifts_ending_at_midnight_do_not_overlap(factories):
    today = today_at_hour(0).date()
    yesterday = yesterday_at_hour(0).date()

    # shift yesterday dpw
    factories.ShiftFactory(start_time=yesterday_at_hour(21), shift_minutes=3 * HOUR)
    # shift today dpw
    factories.ShiftFactory(start_time=today_at_hour(0), shift_minutes=3 * HOUR)

    data = list(shifts_as_grid(Shift.objects.all()))

    assert len(data) == 2

    data_0, data_1 = data

    assert data_0['date'] == yesterday
    assert len(data_0['cells']) == 2  # this is the tabular data, dunno what to assert.

    assert data_1['date'] == today
    assert len(data_1['cells']) == 3  # this is the tabular data, dunno what to assert.


#
# Test merge empties
#
@pytest.mark.django_db
def test_merging_single_set_of_empty_columns(factories):
    SF = factories.ShiftFactory
    shifts = (
        shift_to_dict(SF(start_time=today_at_hour(0),  shift_minutes=6 * HOUR)),
        build_empty_column(start_time=today_at_hour(6), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(7), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(8), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(9), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(10), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(11), minutes=1 * HOUR),
        shift_to_dict(SF(start_time=today_at_hour(12),  shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(18),  shift_minutes=6 * HOUR)),
    )

    merged_shifts = collapse_empty_columns(shifts)
    assert len(merged_shifts) == 4

    assert merged_shifts[1]['shift_minutes'] == 6 * HOUR
    assert not merged_shifts[1]['shifts']
    assert merged_shifts[1]['is_empty']


@pytest.mark.django_db
def test_merging_starting_with_set_of_empty_columns(factories):
    SF = factories.ShiftFactory
    shifts = (
        build_empty_column(start_time=today_at_hour(0), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(1), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(2), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(3), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(4), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(5), minutes=1 * HOUR),
        shift_to_dict(SF(start_time=today_at_hour(6),  shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(12),  shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(18),  shift_minutes=6 * HOUR)),
    )

    merged_shifts = collapse_empty_columns(shifts)
    assert len(merged_shifts) == 4

    assert merged_shifts[0]['shift_minutes'] == 6 * HOUR
    assert not merged_shifts[0]['shifts']
    assert merged_shifts[0]['is_empty']


@pytest.mark.django_db
def test_merging_empties_from_end_of_columns(factories):
    SF = factories.ShiftFactory
    shifts = (
        shift_to_dict(SF(start_time=today_at_hour(0),  shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(6),  shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(12),  shift_minutes=6 * HOUR)),
        build_empty_column(start_time=today_at_hour(18), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(19), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(20), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(21), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(22), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(23), minutes=1 * HOUR),
    )

    merged_shifts = collapse_empty_columns(shifts)
    assert len(merged_shifts) == 4

    assert merged_shifts[3]['shift_minutes'] == 6 * HOUR
    assert not merged_shifts[3]['shifts']
    assert merged_shifts[3]['is_empty']


@pytest.mark.django_db
def test_split_sets_of_empties(factories):
    SF = factories.ShiftFactory
    shifts = (
        build_empty_column(start_time=today_at_hour(0), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(1), minutes=1 * HOUR),
        shift_to_dict(SF(start_time=today_at_hour(2), shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(8), shift_minutes=6 * HOUR)),
        shift_to_dict(SF(start_time=today_at_hour(14), shift_minutes=6 * HOUR)),
        build_empty_column(start_time=today_at_hour(20), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(21), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(22), minutes=1 * HOUR),
        build_empty_column(start_time=today_at_hour(23), minutes=1 * HOUR),
    )

    merged_shifts = collapse_empty_columns(shifts)
    assert len(merged_shifts) == 5

    assert merged_shifts[0]['shift_minutes'] == 2 * HOUR
    assert not merged_shifts[0]['shifts']
    assert merged_shifts[0]['is_empty']

    assert merged_shifts[4]['shift_minutes'] == 4 * HOUR
    assert not merged_shifts[4]['shifts']
    assert merged_shifts[4]['is_empty']
