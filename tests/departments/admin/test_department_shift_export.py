from django.core.urlresolvers import reverse


def test_department_shift_export_page(admin_webtest_client, factories):
    department = factories.DepartmentFactory()

    role_a = factories.RoleFactory()
    role_b = factories.RoleFactory()

    factories.ShiftSlotFactory(shift__role=role_a)
    factories.ShiftSlotFactory(shift__role=role_b)

    url = reverse('admin:department-shift-report', kwargs={'pk': department.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200

    assert 'Content-Disposition' not in response.headers


def test_department_shift_export_download(admin_webtest_client, factories):
    department = factories.DepartmentFactory()

    role_a = factories.RoleFactory()
    role_b = factories.RoleFactory()

    factories.ShiftSlotFactory(shift__role=role_a)
    factories.ShiftSlotFactory(shift__role=role_b)

    url = reverse('admin:department-shift-report', kwargs={'pk': department.pk})
    response = admin_webtest_client.get(url + '?download')
    assert response.status_code == 200

    assert 'Content-Disposition' in response.headers
    assert response.headers['Content-Disposition'].startswith('attachment')
