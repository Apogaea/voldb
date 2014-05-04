from __future__ import unicode_literals
from django.db import models
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
        if self.profile.display_name:
            return self.profile.display_name
        else:
            return obfuscate_email(self.email)
