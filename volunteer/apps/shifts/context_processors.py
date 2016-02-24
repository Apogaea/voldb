from django.db.models import Sum
from django.core.cache import cache

from volunteer.apps.events.utils import get_active_event

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)


SHIFT_STATS_CACHE_KEY = "shift-slots-stats"


def get_cache_key(latest_changed_slot, latest_changed_shift, active_event):
    if latest_changed_slot:
        slot_key = latest_changed_slot.updated_at.isoformat()
    else:
        slot_key = ''

    if latest_changed_shift:
        shift_key = latest_changed_shift.updated_at.isoformat()
    else:
        shift_key = ''

    if active_event:
        event_key = active_event.updated_at.isoformat()
    else:
        event_key = ''

    return ':'.join((
        SHIFT_STATS_CACHE_KEY,
        shift_key,
        slot_key,
        event_key,
    ))


def shift_stats(request):
    latest_changed_slot = ShiftSlot.objects.order_by('-updated_at').first()
    latest_changed_shift = Shift.objects.order_by('-updated_at').first()
    active_event = get_active_event(request.session)
    cache_key = get_cache_key(latest_changed_slot, latest_changed_shift, active_event)
    shift_slot_stats = cache.get(cache_key)
    if shift_slot_stats is None:
        total_shift_slot_count = Shift.objects.filter_to_active_event(
            active_event,
        ).aggregate(
            Sum('num_slots'),
        )['num_slots__sum']
        total_filled_shift_slot_count = ShiftSlot.objects.filter_to_active_event(
            active_event,
        ).filter(
            cancelled_at__isnull=True,
        ).count()

        shift_slot_stats = {
            'SHIFT_STATS': {
                'total_shift_slot_count': total_shift_slot_count,
                'total_filled_shift_slot_count': total_filled_shift_slot_count,
            }
        }
        cache.set(cache_key, shift_slot_stats)
    return shift_slot_stats
