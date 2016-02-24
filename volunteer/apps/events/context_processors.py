from django.core.cache import cache

from volunteer.apps.events.models import (
    Event,
)


EVENT_CHOICES_CACHE_KEY = 'event-choices'


def get_event_choices(active_event_id):
    latest_changed_event = Event.objects.order_by('-updated_at').first()

    if latest_changed_event is None:
        last_update = ''
    else:
        last_update = latest_changed_event.updated_at.isoformat()

    cache_key = ':'.join((
        EVENT_CHOICES_CACHE_KEY,
        last_update,
    ))

    event_choices = cache.get(cache_key)

    if event_choices is None:
        event_choices = tuple((
            (pk, name, str(pk) == str(active_event_id))
            for pk, name in Event.get_event_choices()
        ))
        cache.set(cache_key, event_choices)

    return event_choices


def active_event(request):
    event_id = request.session.get('event_id', None)

    return {
        'EVENT_DATA': {
            'active_event': event_id,
            'event_choices': get_event_choices(event_id),
        },
    }
