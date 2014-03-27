from __future__ import unicode_literals
import datetime

from django.db import models
from django.conf import settings

from departments.models import Department


class Shift(models.Model):
    department = models.ForeignKey(Department, related_name='shifts')
    start_time = models.DateTimeField('shift begins')
    shift_length = models.PositiveSmallIntegerField(default=3)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='shifts')

    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if self.owner:
            return '{0}'.format(
                #this should probably try for a nickname
                #first if one exists
                self.owner,
            )[:7]
        else:
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
