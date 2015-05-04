from django import forms

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
            'start_time',
            'shift_minutes',
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


class AdminShiftSlotCreateForm(BetterModelForm):
    def __init__(self, *args, **kwargs):
        self.shift = kwargs.pop('shift')
        super(AdminShiftSlotCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ShiftSlot
        fields = (
            'volunteer',
        )

    def clean_volunteer(self):
        volunteer = self.cleaned_data['volunteer']
        already_volunteered = self.shift.slots.filter(
            volunteer=volunteer, cancelled_at__isnull=True,
        ).exists()
        if already_volunteered:
            raise forms.ValidationError(
                '{0} is already volunteered for this shift.'.format(volunteer)
            )
        return volunteer
