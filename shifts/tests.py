import datetime

from django.test import TestCase
from django.utils import timezone

from shifts.models import Shift
from departments.factories import DepartmentFactory
from shifts.factories import ShiftFactory, today_at_hour, yesterday_at_hour
from shifts.utils import (
    shifts_to_tabular_data,
    EMPTY_COLUMN,
    get_num_columns,
    group_shifts,
    group_overlapping_shifts,
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


class GroupOverlappingShiftsTest(TestCase):
    def test_non_overlapping(self):
        ShiftFactory(start_time=today_at_hour(0), shift_length=3)
        ShiftFactory(start_time=today_at_hour(3), shift_length=3)
        ShiftFactory(start_time=today_at_hour(6), shift_length=3)
        ShiftFactory(start_time=today_at_hour(9), shift_length=3)
        ShiftFactory(start_time=today_at_hour(12), shift_length=3)
        ShiftFactory(start_time=today_at_hour(15), shift_length=3)
        ShiftFactory(start_time=today_at_hour(18), shift_length=3)
        ShiftFactory(start_time=today_at_hour(21), shift_length=3)

        groups = list(group_overlapping_shifts(Shift.objects.all()))

        self.assertEqual(len(groups), 8)
        self.assertTrue(all(len(g) == 1 for g in groups))

    def test_with_perfectly_overlapping(self):
        # Group 1
        ShiftFactory(start_time=today_at_hour(0), shift_length=6)
        ShiftFactory(start_time=today_at_hour(0), shift_length=6)
        # Group 2
        ShiftFactory(start_time=today_at_hour(6), shift_length=6)
        ShiftFactory(start_time=today_at_hour(6), shift_length=6)
        # Group 3
        ShiftFactory(start_time=today_at_hour(12), shift_length=6)
        ShiftFactory(start_time=today_at_hour(12), shift_length=6)
        # Group 4
        ShiftFactory(start_time=today_at_hour(18), shift_length=6)
        ShiftFactory(start_time=today_at_hour(18), shift_length=6)

        groups = list(group_overlapping_shifts(Shift.objects.all()))

        self.assertEqual(len(groups), 4)
        self.assertTrue(all(len(g) == 2 for g in groups))

    def test_with_partially_overlapping(self):
        # Group 1
        ShiftFactory(start_time=today_at_hour(0), shift_length=6)
        ShiftFactory(start_time=today_at_hour(3), shift_length=6)
        # Group 2
        ShiftFactory(start_time=today_at_hour(12), shift_length=6)
        ShiftFactory(start_time=today_at_hour(15), shift_length=6)
        # Group 3
        ShiftFactory(start_time=today_at_hour(21), shift_length=3)

        groups = list(group_overlapping_shifts(Shift.objects.all()))

        self.assertEqual(len(groups), 3)
        self.assertEqual(len(groups[0]), 2)
        self.assertEqual(len(groups[1]), 2)
        self.assertEqual(len(groups[2]), 1)

    def test_with_staggered_overlaps(self):
        ShiftFactory(start_time=today_at_hour(0), shift_length=3)
        ShiftFactory(start_time=today_at_hour(2), shift_length=3)
        ShiftFactory(start_time=today_at_hour(4), shift_length=3)
        ShiftFactory(start_time=today_at_hour(6), shift_length=3)

        groups = list(group_overlapping_shifts(Shift.objects.all()))

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 4)


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

        today = timezone.now().date()
        yesterday = today - datetime.timedelta(1)

        # shift yesterday dpw
        ShiftFactory(start_time=yesterday_at_hour(12), shift_length=3)
        ShiftFactory(start_time=yesterday_at_hour(15), shift_length=3)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(9), shift_length=3)
        ShiftFactory(start_time=today_at_hour(15), shift_length=3)
        # shift today dpw
        ShiftFactory(start_time=today_at_hour(9), shift_length=6)
        ShiftFactory(start_time=today_at_hour(15), shift_length=6)
        #shifts today greeters
        ShiftFactory(start_time=today_at_hour(6), department=greeters, shift_length=3)
        ShiftFactory(start_time=today_at_hour(12), department=greeters, shift_length=3)

        data = list(group_shifts(Shift.objects.all()))

        self.assertEqual(len(data), 4)

        data_0 = data[0]

        self.assertEqual(data_0['department'], dpw)
        self.assertEqual(data_0['date'], yesterday)
        self.assertEqual(data_0['length'], 3)
        self.assertEqual(len(data_0['tabular']), 20)  # this is the tabular data, dunno what to assert.
