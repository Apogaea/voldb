import datetime

from shifts.utils import (
    pairwise,
    shifts_to_tabular_data,
    EMPTY_COLUMN,
    get_num_columns,
    group_shifts,
    shifts_to_non_overlapping_rows,
    build_shift_column,
)

from tests.factories.shifts import (
    today_at_hour,
    yesterday_at_hour,
)


#
#  Build Shift Column
#
def test_non_midnight_spanning_shift(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3)
    column_data = build_shift_column(shift, datetime.date.today())
    assert column_data.get('columns') == shift.shift_length


def test_span_previous_midnight(factories):
    shift = factories.ShiftFactory(start_time=yesterday_at_hour(23), shift_length=9)
    column_data = build_shift_column(shift, datetime.date.today())
    assert column_data.get('columns') == 8


def test_span_next_midnight(factories):
    shift = factories.ShiftFactory(start_time=today_at_hour(23), shift_length=9)
    column_data = build_shift_column(shift, datetime.date.today())
    assert column_data.get('columns') == 1



def has_overlaps(shifts):
    return any(l.overlaps_with(r) for l, r in pairwise(shifts))


#
# shifts_to_non_overlapping_rows tests
#
def test_has_overlaps_util(factories):
    assert not has_overlaps((
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(3), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3),
    ))
    assert has_overlaps((
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(2), shift_length=3),
    ))

def test_with_no_overlaps(factories):
    shifts = (
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(3), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(12), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(15), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(21), shift_length=3),
    )
    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 1
    assert len(rows[0]) == 8
    assert not all((
        has_overlaps(row) for row in rows
    ))


def test_single_set_of_overlaps(factories):
    shifts = (
        # modulo 0
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(3), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(12), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(15), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(21), shift_length=3),
        # modulo 1
        factories.ShiftFactory(start_time=today_at_hour(1), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(4), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(7), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(10), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(13), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(16), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(19), shift_length=3),
    )

    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 2
    assert len(rows[0]) == 8
    assert len(rows[1]) == 7
    self.assertFalse(all(
        has_overlaps(row) for row in rows
    ))

def test_two_sets_of_overlap(factories):
    shifts = (
        # modulo 0
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(3), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(12), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(15), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(21), shift_length=3),
        # modulo 1
        factories.ShiftFactory(start_time=today_at_hour(1), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(4), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(7), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(10), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(13), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(16), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(19), shift_length=3),
        # modulo 2
        factories.ShiftFactory(start_time=today_at_hour(2), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(5), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(8), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(11), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(14), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(17), shift_length=3),
        factories.ShiftFactory(start_time=today_at_hour(20), shift_length=3),
    )
    rows = list(shifts_to_non_overlapping_rows(shifts))
    assert len(rows) == 3
    assert len(rows[0]) == 8
    assert len(rows[1]) == 7
    assert len(rows[2]) == 7
    self.assertFalse(all(
        has_overlaps(row) for row in rows
    ))


class ShiftsToTabularDataTest(TestCase):
    def test_with_no_shifts(self):
        data = shifts_to_tabular_data([], datetime.date.today())
        assert len(data) == 24

        assert all(d == EMPTY_COLUMN for d in data)
        assert get_num_columns(data) == 24

    def test_with_non_overlapping(self):
        shifts = []
        # shift from 9am to noon
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3))
        # shift from noon to 3pm
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(12), shift_length=3))
        # shift from 6pm to 9pm
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        assert get_num_columns(data) == 24

        empties = data[0:9] + data[11:14] + data[15:]

        assert all(d == EMPTY_COLUMN for d in empties)

        non_empties = data[9], data[10], data[14]

        assert all(d['columns'] == 3 for d in non_empties)

    def test_with_simultaneous_shifts(self):
        shifts = []
        # shift from 6pm to 9pm
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(18), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        assert get_num_columns(data) == 24

    def test_with_overlapping_shifts(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(6), shift_length=3))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(8), shift_length=3))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(10), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        assert get_num_columns(data) == 24

    def test_with_shift_that_spans_previous_midnight(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(factories.ShiftFactory(start_time=yesterday_at_hour(23), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(4), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(9), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(14), shift_length=5))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        assert get_num_columns(data) == 24
        assert len(data) == 9
        assert data[0]['columns'] == 4
        assert all(c['columns'] == 5 for c in data[1:4])
        assert all(c['columns'] == 1 for c in data[4:])

    def test_with_shift_that_spans_upcoming_midnight(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(5), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(10), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(15), shift_length=5))
        shifts.append(factories.ShiftFactory(start_time=today_at_hour(20), shift_length=5))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        assert get_num_columns(data) == 24
        assert len(data) == 9
        assert all(c['columns'] == 1 for c in data[:5])
        assert all(c['columns'] == 5 for c in data[5:8])
        assert data[8]['columns'] == 4


class ShiftsGroupingTest(TestCase):
    def test_grouping(self):
        dpw = DepartmentFactory()
        greeters = DepartmentFactory(name='Greeters')

        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()

        # shift yesterday dpw
        factories.ShiftFactory(start_time=yesterday_at_hour(12), shift_length=3)
        factories.ShiftFactory(start_time=yesterday_at_hour(15), shift_length=3)
        # shift today dpw
        factories.ShiftFactory(start_time=today_at_hour(9), shift_length=3)
        factories.ShiftFactory(start_time=today_at_hour(15), shift_length=3)
        # shift today dpw
        factories.ShiftFactory(start_time=today_at_hour(9), shift_length=6)
        factories.ShiftFactory(start_time=today_at_hour(15), shift_length=6)
        # shifts today greeters
        factories.ShiftFactory(start_time=today_at_hour(6), department=greeters, shift_length=3)
        factories.ShiftFactory(start_time=today_at_hour(12), department=greeters, shift_length=3)

        data = list(group_shifts(Shift.objects.all()))

        assert len(data) == 4

        data_0, data_1, data_2, data_3 = data

        assert data_0['department'] == dpw
        assert data_0['date'] == yesterday
        assert data_0['length'] == 3
        assert len(data_0['tabular']) == 20  # this is the tabular data, dunno what to assert

        assert data_1['department'] == dpw
        assert data_1['date'] == today
        assert data_1['length'] == 3
        assert len(data_1['tabular']) == 20  # this is the tabular data, dunno what to assert

        assert data_2['department'] == dpw
        assert data_2['date'] == today
        assert data_2['length'] == 6
        assert len(data_2['tabular']) == 14  # this is the tabular data, dunno what to assert

        assert data_3['department'] == greeters
        assert data_3['date'] == today
        assert data_3['length'] == 3
        assert len(data_3['tabular']) == 20  # this is the tabular data, dunno what to assert

    def test_complex_grouping_with_shifts_spanning_midnight(self):
        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()
        tomorrow = tomorrow_at_hour(0).date()

        # shift yesterday dpw
        s1 = factories.ShiftFactory(start_time=yesterday_at_hour(11), shift_length=12)
        factories.ShiftFactory(start_time=yesterday_at_hour(23), shift_length=12)
        # shift today dpw
        factories.ShiftFactory(start_time=today_at_hour(11), shift_length=12)
        factories.ShiftFactory(start_time=today_at_hour(23), shift_length=12)
        # shift today dpw
        factories.ShiftFactory(start_time=tomorrow_at_hour(11), shift_length=12)

        data = list(group_shifts(Shift.objects.all()))

        assert len(data) == 3

        data_0, data_1, data_2 = data

        assert data_0['date'] == yesterday
        assert len(data_0['tabular']) == 13  # this is the tabular data, dunno what to assert

        assert data_1['date'] == today
        assert len(data_1['tabular']) == 3  # this is the tabular data, dunno what to assert

        assert data_2['date'] == tomorrow
        assert len(data_2['tabular']) == 3  # this is the tabular data, dunno what to assert

    def test_shifts_ending_at_midnight_do_not_overlap(self):
        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()
        tomorrow = tomorrow_at_hour(0).date()

        # shift yesterday dpw
        factories.ShiftFactory(start_time=yesterday_at_hour(21), shift_length=3)
        # shift today dpw
        factories.ShiftFactory(start_time=today_at_hour(0), shift_length=3)

        data = list(group_shifts(Shift.objects.all()))

        assert len(data) == 2

        data_0, data_1 = data

        assert data_0['date'] == yesterday
        assert len(data_0['tabular']) == 22  # this is the tabular data, dunno what to assert

        assert data_1['date'] == today
        assert len(data_1['tabular']) == 22  # this is the tabular data, dunno what to assert
