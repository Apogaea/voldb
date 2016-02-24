from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

from authtools.models import AbstractEmailUser

from volunteer.apps.accounts.utils import obfuscate_email


@python_2_unicode_compatible
class User(AbstractEmailUser):
    class Meta(AbstractEmailUser.Meta):
        ordering = ('email',)

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def profile(self):
        try:
            return self._profile
        except ObjectDoesNotExist:
            from volunteer.apps.profiles.models import Profile
            return Profile.objects.get_or_create(user=self)[0]

    def get_shifts(self, active_event=None):
        from volunteer.apps.shifts.models import Shift
        if active_event is None:
            from volunteer.apps.events.models import Event
            active_event = Event.objects.get_current()
        shifts = self.shift_slots.filter_to_active_event(
            active_event,
        ).filter(
            cancelled_at__isnull=True,
        ).values_list('shift', flat=True)

        return Shift.objects.filter(pk__in=shifts)

    def __str__(self):
        if self.pk is None:
            return "Unsaved User"
        if self.profile.display_name:
            return self.profile.display_name
        else:
            return obfuscate_email(self.email)


@python_2_unicode_compatible
class VerboseUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        if self.pk is None:
            return "Unsaved User"
        return "{p.full_name} ({p.display_name}) <{s.email}>".format(
            p=self.profile,
            s=self,
        )
