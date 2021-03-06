from __future__ import unicode_literals
import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.utils import timezone
from django.utils import timesince
from django.utils.encoding import python_2_unicode_compatible

from volunteer.core.models import Timestamped

from volunteer.apps.shifts.utils import DENVER_TIMEZONE


class ShiftQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_active_event(self, active_event=None):
        if active_event is None:
            from volunteer.apps.events.models import Event
            active_event = Event.objects.get_current()
        if active_event is None:
            return self
        else:
            return self.filter(event=active_event)


def human_readable_minutes(minutes):
    now = timezone.now()
    return timesince.timeuntil(now + timezone.timedelta(minutes=minutes), now)


@python_2_unicode_compatible
class Shift(Timestamped):
    event = models.ForeignKey(
        'events.Event', related_name='shifts', on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        'departments.Role', related_name='shifts', on_delete=models.PROTECT,
    )

    is_closed = models.BooleanField(
        blank=True, default=False,
        help_text=(
            "This will restrict anyone from claiming slots on this shift."
        ),
    )

    start_time = models.DateTimeField(
        'shift begins',
        help_text=(
            "Format: `YYYY-MM-DD HH:MM` with the hours in 24-hour (military) "
            "format.  (eg, 2pm is 14:00)."
        ),
    )
    SHIFT_MINUTES_CHOICES = tuple((
        (i * 5, human_readable_minutes(i * 5)) for i in range(1, 24 * 12 + 1)
    ))
    shift_minutes = models.PositiveSmallIntegerField(
        "shift length",
        validators=[MaxValueValidator(1440)], choices=SHIFT_MINUTES_CHOICES,
        help_text="The length of the shift",
    )

    num_slots = models.PositiveSmallIntegerField(
        default=1,
        help_text="How many slots does this shift have",
    )

    code = models.CharField(
        max_length=50, blank=True,
        help_text="Leave blank if this shift can be claimed by anyone.",
    )

    objects = ShiftQuerySet.as_manager()

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

    @property
    def claimed_slots(self):
        return self.slots.filter(cancelled_at__isnull=True)

    def get_start_time_display(self):
        return self.start_time.strftime('%H:%M')

    @property
    def end_time(self):
        return self.start_time + datetime.timedelta(minutes=self.shift_minutes)

    def overlaps_with(self, other):
        if self.end_time <= other.start_time:
            return False
        elif self.start_time >= other.end_time:
            return False
        return True

    @property
    def is_protected(self):
        return bool(self.code)

    @property
    def is_locked(self):
        return self.is_closed or not self.event.is_registration_open

    @property
    def is_midnight_spanning(self):
        if self.shift_minutes > 24 * 60:
            return True
        start_hour = self.start_time.astimezone(DENVER_TIMEZONE).hour
        end_hour = self.end_time.astimezone(DENVER_TIMEZONE).hour
        return bool(end_hour) and start_hour > end_hour

    # Permissions Methods
    def is_claimable_by_user(self, user):
        """
        Not locked.
        Has open slots.
        User does not already have a slot.
        """
        if self.is_locked:
            return False
        elif not self.has_open_slots:
            return False
        elif self.claimed_slots.filter(volunteer=user).exists():
            return False
        return True

    @property
    def duration(self):
        return timezone.timedelta(minutes=self.shift_minutes)


class ShiftSlotQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_active_event(self, active_event=None):
        if active_event is None:
            from volunteer.apps.events.models import Event
            active_event = Event.objects.get_current()
        if active_event is None:
            return self
        else:
            return self.filter(shift__event=active_event)


@python_2_unicode_compatible
class ShiftSlot(Timestamped):
    shift = models.ForeignKey('Shift', related_name='slots')
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shift_slots')

    cancelled_at = models.DateTimeField(null=True)

    objects = ShiftSlotQuerySet.as_manager()

    def __str__(self):
        return "{s.shift_id}:{s.volunteer_id}".format(s=self)

    def cancel(self):
        self.is_cancelled = True
        self.save()

    def _is_cancelled_getter(self):
        return bool(self.cancelled_at)

    def _is_cancelled_setter(self, value):
        if bool(value) is bool(self.cancelled_at):
            return
        elif value:
            self.cancelled_at = timezone.now()
        else:
            self.cancelled_at = None

    is_cancelled = property(_is_cancelled_getter, _is_cancelled_setter)

    @property
    def is_locked(self):
        return not self.shift.event.is_registration_open

    #
    # Permissions Methods
    #
    def is_cancelable_by_user(self, user):
        """
        Not locked.
        Not cancelled.
        User is the volunteer or is an admin
        else, not allowed.
        """
        if self.is_cancelled:
            return False
        elif self.is_locked:
            return False
        elif user.pk == self.volunteer_id or user.is_admin:
            return True
        return False
