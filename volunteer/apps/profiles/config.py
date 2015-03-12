from django.apps import AppConfig
from django import dispatch
from django.conf import settings
from django.db.models.signals import (
    post_save,
)


class ProfileConfig(AppConfig):
    name = 'volunteer.apps.profile'
    label = 'profile'
    verbose_name = 'Profile'

    def ready(self):
        # Signals
        from volunteer.apps.profile.receivers import (
            create_volunteer_profile,
        )
        dispatch.receiver(post_save, sender=settings.AUTH_USER_MODEL)(
            create_volunteer_profile,
        )
