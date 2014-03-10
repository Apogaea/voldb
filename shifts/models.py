from django.db import models
from django.conf import settings
from departments.models import Department

class Shift(models.Model):
    department = models.ForeignKey(Department)
    start_time = models.DateTimeField('shift begins')
    shift_length = models.PositiveSmallIntegerField(default=3)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='shifts')
