import datetime
from django.utils import timezone
import factory
from shifts.models import Shift


def today_at_hour(hour):
    return timezone.now().replace(hour=hour)


def yesterday_at_hour(hour):
    when = timezone.now().replace(hour=hour)
    return when - datetime.timedelta(1)


class ShiftFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Shift
    department = factory.SubFactory('departments.factories.DepartmentFactory')
    start_time = factory.LazyAttribute(
        lambda x: today_at_hour(9)
    )
    shift_length = 3
    owner = None
