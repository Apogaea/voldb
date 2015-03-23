from __future__ import unicode_literals
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from volunteer.core.models import Timestamped

from volunteer.apps.shifts.utils import DENVER_TIMEZONE


@python_2_unicode_compatible
class Role(Timestamped):
    department = models.ForeignKey(
        'departments.Department', related_name='roles',
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Shift(Timestamped):
    event = models.ForeignKey(
        'events.Event', related_name='shifts', on_delete=models.PROTECT,
    )
    role = models.ForeignKey('Role', related_name='shifts', on_delete=models.PROTECT)

    start_time = models.DateTimeField('shift begins')
    shift_length = models.PositiveSmallIntegerField(default=3)

    num_slots = models.PositiveSmallIntegerField(default=1)

    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.get_start_time_display()

    @property
    def open_slot_count(self):
        return max(0, self.num_slots - self.slots.filter(cancelled_at__isnull=True).count())

    @property
    def filled_slot_count(self):
        return self.slots.filter(cancelled_at__isnull=True).count()

    @property
    def has_open_slots(self):
        return bool(self.open_slot_count)

    def get_start_time_display(self):
        return self.start_time.strftime('%H:%M')

    @property
    def end_time(self):
        return self.start_time + datetime.timedelta(hours=self.shift_length)

    def overlaps_with(self, other):
        if self.end_time <= other.start_time:
            return False
        elif self.start_time >= other.end_time:
            return False
        return True

    def requires_code(self):
        return bool(self.code)

    @property
    def locked(self):
        return not settings.REGISTRATION_OPEN

    @property
    def is_midnight_spanning(self):
        if self.shift_length > 24:
            return True
        start_hour = self.start_time.astimezone(DENVER_TIMEZONE).hour
        end_hour = self.end_time.astimezone(DENVER_TIMEZONE).hour
        return bool(end_hour) and start_hour > end_hour


@python_2_unicode_compatible
class ShiftSlot(Timestamped):
    shift = models.ForeignKey('Shift', related_name='slots')
    # TODO: either volunteer needs to be nullable or this model needs a
    # validity window.  Either will do.
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shifts')

    cancelled_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{s.shift_id:s.volunteer_id}".format(s=self)

    def cancel(self):
        self.cancelled_at = timezone.now()
        self.save()
