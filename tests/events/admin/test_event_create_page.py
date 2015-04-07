from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms.utils import (
    to_current_timezone,
)


def test_event_list_page(admin_webtest_client, models):
    url = reverse('admin:event-create')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    open_at = to_current_timezone(
        timezone.now().replace(microsecond=0) + timezone.timedelta(10)
    )
    close_at = to_current_timezone(
        timezone.now().replace(microsecond=0) + timezone.timedelta(20)
    )

    response.form['name'] = 'Test Event'
    response.form['registration_open_at'] = open_at.strftime('%Y-%m-%d %H:%M:%S')
    response.form['registration_close_at'] = close_at.strftime('%Y-%m-%d %H:%M:%S')

    form_response = response.form.submit()
    assert form_response.status_code == 302

    created_event = models.Event.objects.get(name='Test Event')
    assert to_current_timezone(created_event.registration_open_at) == open_at
    assert to_current_timezone(created_event.registration_close_at) == close_at
