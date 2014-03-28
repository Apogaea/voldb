from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='_profile')

    full_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)


def create_volunteer_profile(sender, instance, created, raw, **kwargs):
    # Create a user profile when a new user account is created
    if not raw and created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(create_volunteer_profile, sender=settings.AUTH_USER_MODEL)
