import datetime

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms.utils import (
    from_current_timezone,
)


def test_shift_create_page(admin_webtest_client, factories):
    role = factories.RoleFactory()
    url = reverse('admin:shift-create', kwargs={
        'department_pk': role.department_id,
        'role_pk': role.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_shift_create(admin_webtest_client, factories, models):
    event = factories.EventFactory()
    role = factories.RoleFactory()
    url = reverse('admin:shift-create', kwargs={
        'department_pk': role.department_id,
        'role_pk': role.pk,
    })

    shift_time = (
        datetime.datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) +
        timezone.timedelta(10)
    )

    response = admin_webtest_client.get(url)
    response.form['start_time'] = shift_time.strftime('%Y-%m-%d %H:%M:%S')
    response.form['shift_minutes'] = 120
    response.form['num_slots'] = 5
    response.form['code'] = 'test-code'

    form_response = response.form.submit()
    assert form_response.status_code == 302

    shift = models.Shift.objects.get()
    assert shift.role == role
    assert shift.event == event
    assert shift.start_time == from_current_timezone(shift_time)
    assert shift.shift_minutes == 120
    assert shift.num_slots == 5
    assert shift.code == 'test-code'
