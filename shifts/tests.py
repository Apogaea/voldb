from django.test import TestCase

from shifts.factories import ShiftFactory, today_at_hour
from shifts.utils import shifts_to_tabular_data, EMPTY_COLUMN, get_num_columns


# Create your tests here.
class ShiftsToTabularDataTest(TestCase):
    def test_with_no_shifts(self):
        data = shifts_to_tabular_data([])
        self.assertEqual(len(data), 24)

        self.assertTrue(all(d == EMPTY_COLUMN for d in data))
        self.assertEqual(get_num_columns(data), 24)

    def test_with_sparse_shifts(self):
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
