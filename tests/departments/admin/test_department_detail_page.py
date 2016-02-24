from django.core.urlresolvers import reverse


def test_department_detail_page(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    url = reverse('admin:department-detail', kwargs={'pk': department.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_department_editing(admin_webtest_client, factories, models):
    department = factories.DepartmentFactory()
    url = reverse('admin:department-detail', kwargs={'pk': department.pk})

    response = admin_webtest_client.get(url)
    response.forms[1]['name'] = 'New Name'
    response.forms[1]['description'] = 'New Description'

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    updated_department = models.Department.objects.get(pk=department.pk)
    assert updated_department.name == 'New Name'
    assert updated_department.description == 'New Description'
