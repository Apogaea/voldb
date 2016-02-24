def get_active_event(session):
    from volunteer.apps.events.models import Event

    event_id = session.get('event_id', None)
    if event_id is not None:
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            try:
                del session['event_id']
            except KeyError:
                pass

    return Event.objects.get_current()
