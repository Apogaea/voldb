from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms.utils import (
    to_current_timezone,
)


def test_event_list_page(admin_webtest_client, models, factories):
    event = factories.EventFactory()

    url = reverse('admin:event-detail', kwargs={'pk': event.pk})

    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    new_open_at = to_current_timezone(
        event.registration_open_at.replace(microsecond=0) + timezone.timedelta(10)
    )
    new_close_at = to_current_timezone(
        event.registration_close_at.replace(microsecond=0) + timezone.timedelta(20)
    )

    response.forms[1]['name'] = 'New Test Event Name'
    response.forms[1]['registration_open_at'] = new_open_at.strftime('%Y-%m-%d %H:%M:%S')
    response.forms[1]['registration_close_at'] = new_close_at.strftime('%Y-%m-%d %H:%M:%S')

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    updated_event = models.Event.objects.get(name='New Test Event Name')
    assert to_current_timezone(updated_event.registration_open_at) == new_open_at
    assert to_current_timezone(updated_event.registration_close_at) == new_close_at
