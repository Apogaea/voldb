from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from volunteer.core.models import Timestamped


class EventQuerySet(models.QuerySet):
    def get_current(self):
        if settings.CURRENT_EVENT_ID is None:
            return self[0]
        else:
            return self.get(pk=settings.CURRENT_EVENT_ID)


@python_2_unicode_compatible
class Event(Timestamped):
    registration_open_at = models.DateTimeField()
    registration_close_at = models.DateTimeField()

    name = models.CharField(max_length=100)

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return "{s.name}: {s.registration_open_at} - {s.registration_close_at}".format(
            s=self,
        )

    @property
    def is_registration_open(self):
        return self.registration_open_at <= timezone.now() <= self.registration_close_at

    class Meta:
        ordering = (
            '-registration_open_at', '-registration_close_at', 'name',
        )
