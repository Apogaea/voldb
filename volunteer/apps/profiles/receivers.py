from volunteer.apps.profiles.models import Profile


def create_volunteer_profile(sender, instance, created, raw, **kwargs):
    # Create a user profile when a new user account is created
    if not raw and created:
        Profile.objects.get_or_create(user=instance, display_name=None)
