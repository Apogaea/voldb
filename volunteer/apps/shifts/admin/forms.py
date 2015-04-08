from betterforms.forms import BetterModelForm

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
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
            'is_closed',
        )


class AdminShiftSlotCancelForm(BetterModelForm):
    class Meta:
        model = ShiftSlot
        fields = tuple()

    def save(self, *args, **kwargs):
        self.instance.is_cancelled = True
        self.instance.save()
        return self.instance
