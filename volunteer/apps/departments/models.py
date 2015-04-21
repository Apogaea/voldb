from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from volunteer.core.models import Timestamped


class DepartmentQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_current_event(self):
        from volunteer.apps.events.models import Event
        current_event = Event.objects.get_current()
        if current_event is None:
            return self
        else:
            return self.filter(roles__shifts__event=current_event).distinct()


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    active_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='lead',
    )
    active_liaison = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='liason',
    )

    objects = DepartmentQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    @property
    def total_shift_slots(self):
        from volunteer.apps.shifts.models import Shift
        return Shift.objects.filter_to_current_event().filter(
            role__department=self,
        ).aggregate(
            Sum('num_slots'),
        )['num_slots__sum']

    @property
    def total_filled_shift_slots(self):
        from volunteer.apps.shifts.models import ShiftSlot
        return ShiftSlot.objects.filter_to_current_event().filter(
            shift__role__department=self,
            cancelled_at__isnull=True,
        ).count()


class RoleQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_current_event(self):
        from volunteer.apps.events.models import Event
        current_event = Event.objects.get_current()
        if current_event is None:
            return self
        else:
            return self.filter(shifts__event=current_event).distinct()


@python_2_unicode_compatible
class Role(Timestamped):
    department = models.ForeignKey(
        'departments.Department', related_name='roles',
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()

    objects = RoleQuerySet.as_manager()

    def __str__(self):
        return self.name
