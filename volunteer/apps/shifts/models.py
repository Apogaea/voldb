from __future__ import unicode_literals
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

from volunteer.apps.shifts.utils import DENVER_TIMEZONE


class Role(models.Model):
    department = models.ForeignKey('departments.Department',
                                   related_name='roles')
    name = models.CharField(max_length=255)
    description = models.TextField()


class Shift(models.Model):
    role = models.ForeignKey('Role', related_name='shifts')

    start_time = models.DateTimeField('shift begins')
    shift_length = models.PositiveSmallIntegerField(default=3)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='shifts',
    )

    code = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        if self.owner:
            # this should probably try for a nickname
            # first if one exists
            return '{0}'.format(
                self.owner,
            )[:7]
        else:
            return self.get_start_time_display()

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


class ShiftHistory(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    shift = models.ForeignKey('Shift', related_name='history')
    ACTION_CLAIM = 'claim'
    ACTION_RELEASE = 'release'
    ACTION_CHOICES = (
        (ACTION_CLAIM, 'Claim'),
        (ACTION_RELEASE, 'Release'),
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
