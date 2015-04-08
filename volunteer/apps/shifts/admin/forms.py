from betterforms.forms import BetterModelForm

from volunteer.apps.shifts.models import (
    Shift,
)


class AdminShiftCreateForm(BetterModelForm):
    class Meta:
        model = Shift
        fields = (
            'start_time',
            'shift_minutes',
            'num_slots',
            'code',
        )


class AdminShiftUpdateForm(BetterModelForm):
    class Meta:
        model = Shift
        fields = (
            'num_slots',
            'code',
        )
