from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='_profile')

    full_name = models.CharField(
        max_length=100, help_text=(
            "Please provide us with your full legal name."
        ),
    )
    display_name = models.CharField(
        max_length=64, unique=True, null=True, help_text=(
            "This will be the name that is publicly displayed to other users "
            "when browsing shifts"
        ),
    )
    phone = models.CharField(max_length=16)

    has_ticket = models.BooleanField('I have a ticket', default=False, blank=True)
