from django.db.models import Sum
from django.core.cache import cache

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)


SHIFT_STATS_CACHE_KEY = "shift-slots-stats"


def shift_stats(request):
    shift_slot_stats = cache.get(SHIFT_STATS_CACHE_KEY)
    if shift_slot_stats is None:
        total_shift_slot_count = Shift.objects.filter_to_current_event().aggregate(
            Sum('num_slots'),
        )['num_slots__sum']
        total_filled_shift_slot_count = ShiftSlot.objects.filter_to_current_event().filter(
            cancelled_at__isnull=True,
        ).count()

        shift_slot_stats = {
            'SHIFT_STATS': {
                'total_shift_slot_count': total_shift_slot_count,
                'total_filled_shift_slot_count': total_filled_shift_slot_count,
            }
        }
        cache.set(SHIFT_STATS_CACHE_KEY, shift_slot_stats)
    return shift_slot_stats
