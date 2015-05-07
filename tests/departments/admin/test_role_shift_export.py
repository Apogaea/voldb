from django.core.urlresolvers import reverse


def test_role_shift_export_page(admin_webtest_client, factories):
    role = factories.RoleFactory()

    factories.ShiftSlotFactory(shift__role=role)
    factories.ShiftSlotFactory(shift__role=role)

    url = reverse(
        'admin:role-shift-report',
        kwargs={'department_pk': role.department_id, 'pk': role.pk},
    )
    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    assert 'Content-Disposition' not in response.headers


def test_role_shift_export_download(admin_webtest_client, factories):
    role = factories.RoleFactory()

    factories.ShiftSlotFactory(shift__role=role)
    factories.ShiftSlotFactory(shift__role=role)

    url = reverse(
        'admin:role-shift-report',
        kwargs={'department_pk': role.department_id, 'pk': role.pk},
    )
    response = admin_webtest_client.get(url + '?download')
    assert response.status_code == 200

    assert 'Content-Disposition' in response.headers
    assert response.headers['Content-Disposition'].startswith('attachment')
