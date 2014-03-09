from django.test import TestCase
from shifts.utils import shifts_to_tabular_data


# Create your tests here.
class ShiftsToTabularDataTest(TestCase):
	def test_with_no_shifts(self):
		data = shifts_to_tabular_data([])
		self.assertEqual(len(data), 24)  
	
