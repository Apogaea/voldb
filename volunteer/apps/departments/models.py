from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from volunteer.core.models import Timestamped


class DepartmentQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_active_event(self, active_event=None):
        if active_event is None:
            from volunteer.apps.events.models import Event
            active_event = Event.objects.get_current()
        if active_event is None:
            return self
        else:
            return self.filter(roles__shifts__event=active_event).distinct()


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    objects = DepartmentQuerySet.as_manager()

    leads = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='departments'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def user_can_admin(self, user):
        if user.is_staff or user.is_superuser:
            return True
        elif self.leads.filter(pk=user.pk).exists():
            return True
        return False

    def total_shift_slots(self, active_event):
        from volunteer.apps.shifts.models import Shift
        return Shift.objects.filter_to_active_event(active_event).filter(
            role__department=self,
        ).aggregate(
            Sum('num_slots'),
        )['num_slots__sum']

    def total_filled_shift_slots(self, active_event):
        from volunteer.apps.shifts.models import ShiftSlot
        return ShiftSlot.objects.filter_to_active_event(active_event).filter(
            shift__role__department=self,
            cancelled_at__isnull=True,
        ).count()


class RoleQuerySet(models.QuerySet):
    use_for_related_fields = True

    def filter_to_active_event(self, active_event=None):
        if active_event is None:
            from volunteer.apps.events.models import Event
            active_event = Event.objects.get_current()
        if active_event is None:
            return self
        else:
            return self.filter(shifts__event=active_event).distinct()


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

    def total_shift_slots(self, active_event):
        from volunteer.apps.shifts.models import Shift
        return Shift.objects.filter_to_active_event(active_event).filter(
            role=self,
        ).aggregate(
            Sum('num_slots'),
        )['num_slots__sum']

    def total_filled_shift_slots(self, active_event):
        from volunteer.apps.shifts.models import ShiftSlot
        return ShiftSlot.objects.filter_to_active_event(active_event).filter(
            shift__role=self,
            cancelled_at__isnull=True,
        ).count()
