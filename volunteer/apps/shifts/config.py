from django.apps import AppConfig
from django import dispatch
from django.db.models.signals import (
    pre_save,
)


class ShiftsConfig(AppConfig):
    name = 'volunteer.apps.shifts'
    label = 'shifts'
    verbose_name = 'Shifts'

    def ready(self):
        # Signals
        from volunteer.apps.shifts.receivers import (
            track_shift_history,
        )
        dispatch.receiver(pre_save, sender='shifts.Shift')(
            track_shift_history,
        )
