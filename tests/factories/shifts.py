import datetime
import factory

from volunteer.apps.shifts.models import (
    Shift,
    Role,
)
from volunteer.apps.shifts.utils import DENVER_TIMEZONE


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
    name = factory.Sequence("role-{0}".format)
    description = "Role Description"
    department = factory.SubFactory('tests.factories.departments.DepartmentFactory')

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
