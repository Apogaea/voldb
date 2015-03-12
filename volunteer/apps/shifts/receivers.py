from volunteer.apps.shifts.models import (
    Shift,
    ShiftHistory,
)


def track_shift_history(sender, instance, raw, **kwargs):
    """
    Each time a shift is saved, check to see if the owner is being claimed.  If
    it is, track the change.
    """
    if not instance.pk or raw:
        return
    shift = Shift.objects.get(pk=instance.pk)
    if not shift.owner == instance.owner:
        if instance.owner is None:
            action = ShiftHistory.ACTION_RELEASE
        else:
            action = ShiftHistory.ACTION_CLAIM
        ShiftHistory.objects.create(
            shift=instance,
            user=instance.owner or shift.owner,
            action=action,
        )
