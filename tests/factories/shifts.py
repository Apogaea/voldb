import datetime
import factory

from django.utils import timezone

from volunteer.apps.shifts.models import (
    Shift,
    Role,
    ShiftSlot,
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


def get_default_event(*args, **kwargs):
    from volunteer.apps.events.models import Event
    current_event = Event.objects.get_current()
    if current_event is None:
        open_at = timezone.now().replace(
            year=2014, month=3, day=1, hour=0, minute=0, second=0, microsecond=0,
        )
        close_at = timezone.now().replace(
            year=2014, month=5, day=1, hour=0, minute=0, second=0, microsecond=0,
        )

        current_event = Event.objects.create(
            name="Apogaea 2014",
            registration_open_at=open_at,
            registration_close_at=close_at,
        )
    return current_event


class ShiftFactory(factory.DjangoModelFactory):
    event = factory.LazyAttribute(get_default_event)
    role = factory.SubFactory(RoleFactory)
    start_time = factory.LazyAttribute(
        lambda x: today_at_hour(9)
    )
    shift_length = 3
    code = ''

    class Meta:
        model = Shift


class ShiftSlotFactory(factory.DjangoModelFactory):
    shift = factory.SubFactory(ShiftFactory)
    volunteer = factory.SubFactory('tests.factories.accounts.UserFactory')

    cancelled_at = None

    class Meta:
        model = ShiftSlot


class CancelledShiftSlotFactory(ShiftSlotFactory):
    cancelled_at = factory.LazyAttribute(lambda x: timezone.now())
