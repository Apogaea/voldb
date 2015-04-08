from django.core.urlresolvers import reverse


def test_shift_detail_page(admin_webtest_client, factories):
    shift = factories.ShiftFactory()
    url = reverse('admin:shift-detail', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_shift_editing(admin_webtest_client, factories, models):
    shift = factories.ShiftFactory(num_slots=1, code='test')
    url = reverse('admin:shift-detail', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })

    response = admin_webtest_client.get(url)
    response.form['num_slots'] = 5
    response.form['code'] = 'test-code-update'

    form_response = response.form.submit()
    assert form_response.status_code == 302

    updated_shift = models.Shift.objects.get(pk=shift.pk)
    assert updated_shift.num_slots == 5
    assert updated_shift.code == 'test-code-update'
