def test_get_current_event_when_setting_not_set(settings, models):
    settings.CURRENT_EVENT_ID = None
    # sanity
    assert models.Event.objects.exists()
    latest_event = models.Event.objects.last()
    event = models.Event.objects.get_current()
    assert latest_event == event


def test_get_current_event_when_set(settings, models, factories):
    factories.FutureEventFactory()
    current_event = factories.EventFactory()
    settings.CURRENT_EVENT_ID = current_event.pk
    assert models.Event.objects.count() > 1
    event = models.Event.objects.get_current()
    assert current_event == event
