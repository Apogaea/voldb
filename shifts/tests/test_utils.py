import datetime

from django.test import TestCase

from shifts.models import Shift
from departments.factories import DepartmentFactory
from shifts.factories import (
    ShiftFactory, today_at_hour, yesterday_at_hour, tomorrow_at_hour,
)
from shifts.utils import (
    pairwise,
    shifts_to_tabular_data,
    EMPTY_COLUMN,
    get_num_columns,
    group_shifts,
    shifts_to_non_overlapping_rows,
    build_shift_column,
)


class OverlapsMethodTest(TestCase):
    def test_non_overlapping_adjacent_shifts(self):
        shift_a = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        shift_b = ShiftFactory(start_time=today_at_hour(9), shift_length=3)

        self.assertFalse(shift_a.overlaps_with(shift_b))
        self.assertFalse(shift_b.overlaps_with(shift_a))

    def test_non_overlapping_separated_shifts(self):
        shift_a = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        shift_b = ShiftFactory(start_time=today_at_hour(10), shift_length=3)

        self.assertFalse(shift_a.overlaps_with(shift_b))
        self.assertFalse(shift_b.overlaps_with(shift_a))

    def test_intersection(self):
        shift_a = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        shift_b = ShiftFactory(start_time=today_at_hour(8), shift_length=3)

        self.assertTrue(shift_a.overlaps_with(shift_b))
        self.assertTrue(shift_b.overlaps_with(shift_a))

    def test_fully_contained(self):
        shift_a = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        shift_b = ShiftFactory(start_time=today_at_hour(7), shift_length=1)

        self.assertTrue(shift_a.overlaps_with(shift_b))
        self.assertTrue(shift_b.overlaps_with(shift_a))


class BuildShiftColumnTest(TestCase):
    def test_non_midnight_spanning_shift(self):
        shift = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        column_data = build_shift_column(shift, datetime.date.today())
        self.assertEqual(column_data.get('columns'), shift.shift_length)

    def test_span_previous_midnight(self):
        shift = ShiftFactory(start_time=yesterday_at_hour(23), shift_length=9)
        column_data = build_shift_column(shift, datetime.date.today())
        self.assertEqual(column_data.get('columns'), 8)

    def test_span_next_midnight(self):
        shift = ShiftFactory(start_time=today_at_hour(23), shift_length=9)
        column_data = build_shift_column(shift, datetime.date.today())
        self.assertEqual(column_data.get('columns'), 1)


class SpansMidnightPropertyTest(TestCase):
    def test_doesnt_span_midnight(self):
        shift = ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        self.assertFalse(shift.is_midnight_spanning)

    def test_does_span_midnight(self):
        shift = ShiftFactory(start_time=today_at_hour(23), shift_length=3)
        self.assertTrue(shift.is_midnight_spanning)

    def test_really_long_shift(self):
        shift = ShiftFactory(start_time=today_at_hour(23), shift_length=26)
        self.assertTrue(shift.is_midnight_spanning)

    def test_ends_at_midnight(self):
        shift = ShiftFactory(start_time=today_at_hour(21), shift_length=3)
        self.assertFalse(shift.is_midnight_spanning)


def has_overlaps(shifts):
    return any(l.overlaps_with(r) for l, r in pairwise(shifts))


class ShiftsToNonOverlappingRowsTest(TestCase):
    def test_has_overlaps_util(self):
        self.assertFalse(has_overlaps((
            ShiftFactory(start_time=today_at_hour(0), shift_length=3),
            ShiftFactory(start_time=today_at_hour(3), shift_length=3),
            ShiftFactory(start_time=today_at_hour(6), shift_length=3),
        )))
        self.assertTrue(has_overlaps((
            ShiftFactory(start_time=today_at_hour(0), shift_length=3),
            ShiftFactory(start_time=today_at_hour(2), shift_length=3),
        )))

    def test_with_no_overlaps(self):
        shifts = (
            ShiftFactory(start_time=today_at_hour(0), shift_length=3),
            ShiftFactory(start_time=today_at_hour(3), shift_length=3),
            ShiftFactory(start_time=today_at_hour(6), shift_length=3),
            ShiftFactory(start_time=today_at_hour(9), shift_length=3),
            ShiftFactory(start_time=today_at_hour(12), shift_length=3),
            ShiftFactory(start_time=today_at_hour(15), shift_length=3),
            ShiftFactory(start_time=today_at_hour(18), shift_length=3),
            ShiftFactory(start_time=today_at_hour(21), shift_length=3),
        )
        rows = list(shifts_to_non_overlapping_rows(shifts))
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0]), 8)
        self.assertFalse(all(
            has_overlaps(row) for row in rows
        ))

    def test_single_set_of_overlaps(self):
        shifts = (
            # modulo 0
            ShiftFactory(start_time=today_at_hour(0), shift_length=3),
            ShiftFactory(start_time=today_at_hour(3), shift_length=3),
            ShiftFactory(start_time=today_at_hour(6), shift_length=3),
            ShiftFactory(start_time=today_at_hour(9), shift_length=3),
            ShiftFactory(start_time=today_at_hour(12), shift_length=3),
            ShiftFactory(start_time=today_at_hour(15), shift_length=3),
            ShiftFactory(start_time=today_at_hour(18), shift_length=3),
            ShiftFactory(start_time=today_at_hour(21), shift_length=3),
            # modulo 1
            ShiftFactory(start_time=today_at_hour(1), shift_length=3),
            ShiftFactory(start_time=today_at_hour(4), shift_length=3),
            ShiftFactory(start_time=today_at_hour(7), shift_length=3),
            ShiftFactory(start_time=today_at_hour(10), shift_length=3),
            ShiftFactory(start_time=today_at_hour(13), shift_length=3),
            ShiftFactory(start_time=today_at_hour(16), shift_length=3),
            ShiftFactory(start_time=today_at_hour(19), shift_length=3),
        )

        rows = list(shifts_to_non_overlapping_rows(shifts))
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(rows[0]), 8)
        self.assertEqual(len(rows[1]), 7)
        self.assertFalse(all(
            has_overlaps(row) for row in rows
        ))

    def test_two_sets_of_overlap(self):
        shifts = (
            # modulo 0
            ShiftFactory(start_time=today_at_hour(0), shift_length=3),
            ShiftFactory(start_time=today_at_hour(3), shift_length=3),
            ShiftFactory(start_time=today_at_hour(6), shift_length=3),
            ShiftFactory(start_time=today_at_hour(9), shift_length=3),
            ShiftFactory(start_time=today_at_hour(12), shift_length=3),
            ShiftFactory(start_time=today_at_hour(15), shift_length=3),
            ShiftFactory(start_time=today_at_hour(18), shift_length=3),
            ShiftFactory(start_time=today_at_hour(21), shift_length=3),
            # modulo 1
            ShiftFactory(start_time=today_at_hour(1), shift_length=3),
            ShiftFactory(start_time=today_at_hour(4), shift_length=3),
            ShiftFactory(start_time=today_at_hour(7), shift_length=3),
            ShiftFactory(start_time=today_at_hour(10), shift_length=3),
            ShiftFactory(start_time=today_at_hour(13), shift_length=3),
            ShiftFactory(start_time=today_at_hour(16), shift_length=3),
            ShiftFactory(start_time=today_at_hour(19), shift_length=3),
            # modulo 2
            ShiftFactory(start_time=today_at_hour(2), shift_length=3),
            ShiftFactory(start_time=today_at_hour(5), shift_length=3),
            ShiftFactory(start_time=today_at_hour(8), shift_length=3),
            ShiftFactory(start_time=today_at_hour(11), shift_length=3),
            ShiftFactory(start_time=today_at_hour(14), shift_length=3),
            ShiftFactory(start_time=today_at_hour(17), shift_length=3),
            ShiftFactory(start_time=today_at_hour(20), shift_length=3),
        )
        rows = list(shifts_to_non_overlapping_rows(shifts))
        self.assertEqual(len(rows), 3)
        self.assertEqual(len(rows[0]), 8)
        self.assertEqual(len(rows[1]), 7)
        self.assertEqual(len(rows[2]), 7)
        self.assertFalse(all(
            has_overlaps(row) for row in rows
        ))


class ShiftsToTabularDataTest(TestCase):
    def test_with_no_shifts(self):
        data = shifts_to_tabular_data([], datetime.date.today())
        self.assertEqual(len(data), 24)

        self.assertTrue(all(d == EMPTY_COLUMN for d in data))
        self.assertEqual(get_num_columns(data), 24)

    def test_with_non_overlapping(self):
        shifts = []
        # shift from 9am to noon
        shifts.append(ShiftFactory(start_time=today_at_hour(9), shift_length=3))
        # shift from noon to 3pm
        shifts.append(ShiftFactory(start_time=today_at_hour(12), shift_length=3))
        # shift from 6pm to 9pm
        shifts.append(ShiftFactory(start_time=today_at_hour(18), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        self.assertEqual(get_num_columns(data), 24)

        empties = data[0:9] + data[11:14] + data[15:]

        self.assertTrue(all(d == EMPTY_COLUMN for d in empties))

        non_empties = data[9], data[10], data[14]

        self.assertTrue(all(d['columns'] == 3 for d in non_empties))

    def test_with_simultaneous_shifts(self):
        shifts = []
        # shift from 6pm to 9pm
        shifts.append(ShiftFactory(start_time=today_at_hour(18), shift_length=3))
        shifts.append(ShiftFactory(start_time=today_at_hour(18), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        self.assertEqual(get_num_columns(data), 24)

    def test_with_overlapping_shifts(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(ShiftFactory(start_time=today_at_hour(6), shift_length=3))
        shifts.append(ShiftFactory(start_time=today_at_hour(8), shift_length=3))
        shifts.append(ShiftFactory(start_time=today_at_hour(10), shift_length=3))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        self.assertEqual(get_num_columns(data), 24)

    def test_with_shift_that_spans_previous_midnight(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(ShiftFactory(start_time=yesterday_at_hour(23), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(4), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(9), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(14), shift_length=5))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        self.assertEqual(get_num_columns(data), 24)
        self.assertEqual(len(data), 9)
        self.assertEqual(data[0]['columns'], 4)
        self.assertTrue(all(c['columns'] == 5 for c in data[1:4]))
        self.assertTrue(all(c['columns'] == 1 for c in data[4:]))

    def test_with_shift_that_spans_upcoming_midnight(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(ShiftFactory(start_time=today_at_hour(5), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(10), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(15), shift_length=5))
        shifts.append(ShiftFactory(start_time=today_at_hour(20), shift_length=5))

        data = shifts_to_tabular_data(shifts, datetime.date.today())
        self.assertEqual(get_num_columns(data), 24)
        self.assertEqual(len(data), 9)
        self.assertTrue(all(c['columns'] == 1 for c in data[:5]))
        self.assertTrue(all(c['columns'] == 5 for c in data[5:8]))
        self.assertEqual(data[8]['columns'], 4)


class ShiftsGroupingTest(TestCase):
    def test_grouping(self):
        dpw = DepartmentFactory()
        greeters = DepartmentFactory(name='Greeters')

        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()

        # shift yesterday dpw
        ShiftFactory(start_time=yesterday_at_hour(12), shift_length=3)
        ShiftFactory(start_time=yesterday_at_hour(15), shift_length=3)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(9), shift_length=3)
        ShiftFactory(start_time=today_at_hour(15), shift_length=3)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(9), shift_length=6)
        ShiftFactory(start_time=today_at_hour(15), shift_length=6)
        # shifts today greeters
        ShiftFactory(start_time=today_at_hour(6), department=greeters, shift_length=3)
        ShiftFactory(start_time=today_at_hour(12), department=greeters, shift_length=3)

        data = list(group_shifts(Shift.objects.all()))

        self.assertEqual(len(data), 4)

        data_0, data_1, data_2, data_3 = data

        self.assertEqual(data_0['department'], dpw)
        self.assertEqual(data_0['date'], yesterday)
        self.assertEqual(data_0['length'], 3)
        self.assertEqual(len(data_0['tabular']), 20)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_1['department'], dpw)
        self.assertEqual(data_1['date'], today)
        self.assertEqual(data_1['length'], 3)
        self.assertEqual(len(data_1['tabular']), 20)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_2['department'], dpw)
        self.assertEqual(data_2['date'], today)
        self.assertEqual(data_2['length'], 6)
        self.assertEqual(len(data_2['tabular']), 14)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_3['department'], greeters)
        self.assertEqual(data_3['date'], today)
        self.assertEqual(data_3['length'], 3)
        self.assertEqual(len(data_3['tabular']), 20)  # this is the tabular data, dunno what to assert.

    def test_complex_grouping_with_shifts_spanning_midnight(self):
        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()
        tomorrow = tomorrow_at_hour(0).date()

        # shift yesterday dpw
        s1 = ShiftFactory(start_time=yesterday_at_hour(11), shift_length=12)
        ShiftFactory(start_time=yesterday_at_hour(23), shift_length=12)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(11), shift_length=12)
        ShiftFactory(start_time=today_at_hour(23), shift_length=12)
        # shift today dpw
        ShiftFactory(start_time=tomorrow_at_hour(11), shift_length=12)

        data = list(group_shifts(Shift.objects.all()))

        self.assertEqual(len(data), 3)

        data_0, data_1, data_2 = data

        self.assertEqual(data_0['date'], yesterday)
        self.assertEqual(len(data_0['tabular']), 13)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_1['date'], today)
        self.assertEqual(len(data_1['tabular']), 3)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_2['date'], tomorrow)
        self.assertEqual(len(data_2['tabular']), 3)  # this is the tabular data, dunno what to assert.

    def test_shifts_ending_at_midnight_do_not_overlap(self):
        today = today_at_hour(0).date()
        yesterday = yesterday_at_hour(0).date()
        tomorrow = tomorrow_at_hour(0).date()

        # shift yesterday dpw
        ShiftFactory(start_time=yesterday_at_hour(21), shift_length=3)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(0), shift_length=3)

        data = list(group_shifts(Shift.objects.all()))

        self.assertEqual(len(data), 2)

        data_0, data_1 = data

        self.assertEqual(data_0['date'], yesterday)
        self.assertEqual(len(data_0['tabular']), 22)  # this is the tabular data, dunno what to assert.

        self.assertEqual(data_1['date'], today)
        self.assertEqual(len(data_1['tabular']), 22)  # this is the tabular data, dunno what to assert.
