import datetime
import factory

from shifts.models import Shift
from shifts.utils import DENVER_TIMEZONE


def today_at_hour(hour):
    return datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(hour=hour, tzinfo=DENVER_TIMEZONE),
    )


def yesterday_at_hour(hour):
    return today_at_hour(hour) - datetime.timedelta(1)


def tomorrow_at_hour(hour):
    return today_at_hour(hour) + datetime.timedelta(1)


class ShiftFactory(factory.DjangoModelFactory):
    department = factory.SubFactory('departments.factories.DepartmentFactory')
    start_time = factory.LazyAttribute(
        lambda x: today_at_hour(9)
    )
    shift_length = 3
    owner = None
    code = ''

    class Meta:
        model = Shift
