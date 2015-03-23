from django.db import models

from volunteer.core.models import Timestamped


class Event(Timestamped):
    registration_open_at = models.DateTimeField()
    registration_close_at = models.DateTimeField()

    name = models.CharField(max_length=100)
