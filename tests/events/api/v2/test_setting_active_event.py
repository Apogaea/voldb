from django.core.urlresolvers import reverse


def test_setting_active_event_api_endpoint(factories, api_client):
    factories.FutureEventFactory(name='A')
    event_b = factories.PastEventFactory(name='B')

    select_url = reverse('v2:event-select-active')

    assert api_client.session.get('event_id', None) is None

    response = api_client.post(select_url, {'active_event': event_b.pk})

    assert response.status_code == 204
    assert api_client.session.get('event_id', None) == str(event_b.pk)


def test_setting_default_unsets_active_event(factories, api_client):
    factories.FutureEventFactory(name='A')
    event_b = factories.PastEventFactory(name='B')

    select_url = reverse('v2:event-select-active')

    api_client.session['event_id'] = event_b.pk

    response = api_client.post(select_url, {'active_event': None})
    assert response.status_code == 204

    assert api_client.session.get('event_id', None) is None


def test_error_on_invalid_choice_for_active_event(factories, api_client):
    factories.FutureEventFactory(name='A')
    event_b = factories.PastEventFactory(name='B')

    select_url = reverse('v2:event-select-active')

    api_client.session['event_id'] = event_b.pk

    response = api_client.post(select_url, {'active_event': 1234567890})
    assert response.status_code == 400
