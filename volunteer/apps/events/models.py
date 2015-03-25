from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from volunteer.core.models import Timestamped


@python_2_unicode_compatible
class Event(Timestamped):
    registration_open_at = models.DateTimeField()
    registration_close_at = models.DateTimeField()

    name = models.CharField(max_length=100)

    def __str__(self):
        return "{s.name}: {s.registration_open_at} - {s.registration_close_at}".format(
            s=self,
        )

    @property
    def is_registration_open(self):
        return self.registration_open_at <= timezone.now() <= self.registration_close_at
