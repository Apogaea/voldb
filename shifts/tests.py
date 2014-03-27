from django.test import TestCase

from shifts.models import Shift
from departments.factories import DepartmentFactory
from shifts.factories import ShiftFactory, today_at_hour, yesterday_at_hour
from shifts.utils import (
    pairwise,
    shifts_to_tabular_data,
    EMPTY_COLUMN,
    get_num_columns,
    group_shifts,
    shifts_to_non_overlapping_rows,
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
        data = shifts_to_tabular_data([])
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

        data = shifts_to_tabular_data(shifts)
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

        data = shifts_to_tabular_data(shifts)
        self.assertEqual(get_num_columns(data), 24)

    def test_with_overlapping_shifts(self):
        shifts = []
        # 3 hour shifts, staggered 2 hours apart.
        shifts.append(ShiftFactory(start_time=today_at_hour(6), shift_length=3))
        shifts.append(ShiftFactory(start_time=today_at_hour(8), shift_length=3))
        shifts.append(ShiftFactory(start_time=today_at_hour(10), shift_length=3))

        data = shifts_to_tabular_data(shifts)
        self.assertEqual(get_num_columns(data), 24)


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
