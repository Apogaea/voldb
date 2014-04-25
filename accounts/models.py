from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from authtools.models import AbstractEmailUser

from accounts.utils import obfuscate_email


class User(AbstractEmailUser):
    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def profile(self):
        try:
            return self._profile
        except ObjectDoesNotExist:
            from profiles.models import Profile
            return Profile.objects.get_or_create(user=self)[0]

    def __unicode__(self):
        return str(self)

    def __str__(self):
        try:
            profile = self._profile
        except ObjectDoesNotExist:
            return obfuscate_email(self.email)
        else:
            return profile.display_name or obfuscate_email(self.email)


def create_volunteer_profile(sender, instance, created, raw, **kwargs):
    # Create a user profile when a new user account is created
    if not raw and created:
        from profiles.models import Profile
        Profile.objects.get_or_create(user=instance)

post_save.connect(create_volunteer_profile, sender=User)
