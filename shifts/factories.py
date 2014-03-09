import datetime
from django.utils import timezone
import factory
from shifts.models import Shift


class ShiftFactory(factory.DjangoModelFactory):
	FACTORY_FOR = shifts
    department = 
    start_time = factory.LazyAttribute(
    	lambda x: datetime.datetime.combine(timezone.now(), datetime.time(hour=9))
    )
    shift_length = 3
    owner = None