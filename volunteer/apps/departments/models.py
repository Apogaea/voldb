from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


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
