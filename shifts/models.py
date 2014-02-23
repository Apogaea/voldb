from django.db import models
from django.conf import settings
from departments.models import Department

# Create your models here.
class Shift(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    start_time = models.DateTimeField('shift begins')
    shift_length = models.PositiveSmallIntegerField(default=3)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='owner')
    def __str__(self):
        return self.name