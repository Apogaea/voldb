from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
