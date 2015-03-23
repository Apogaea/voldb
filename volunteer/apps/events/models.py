from django.db import models
from django.utils import timezone

from volunteer.core.models import Timestamped


class Event(Timestamped):
    registration_open_at = models.DateTimeField()
    registration_close_at = models.DateTimeField()

    name = models.CharField(max_length=100)

    @property
    def is_registration_open(self):
        return self.registration_open_at <= timezone.now() <= self.registration_close_at
