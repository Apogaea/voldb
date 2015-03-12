from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='_profile')

    full_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)

    has_ticket = models.BooleanField('I have a ticket', default=False, blank=True)
