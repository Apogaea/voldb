import datetime
import factory

from shifts.models import (
    Shift,
    Role,
)
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


class RoleFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "role-{0}".format(n))
    description = "Role Description"
    department = factory.SubFactory('departments.factories.DepartmentFactory')

    class Meta:
        model = Role


class ShiftFactory(factory.DjangoModelFactory):
    role = factory.SubFactory(RoleFactory)
    start_time = factory.LazyAttribute(
        lambda x: today_at_hour(9)
    )
    shift_length = 3
    owner = None
    code = ''

    class Meta:
        model = Shift
