from django.core.urlresolvers import reverse


def test_role_create_page(admin_webtest_client, factories):
    role = factories.RoleFactory()
    url = reverse('admin:role-create', kwargs={
        'department_pk': role.department_id,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_role_creation(admin_webtest_client, factories, models):
    department = factories.DepartmentFactory()
    url = reverse('admin:role-create', kwargs={
        'department_pk': department.pk,
    })

    response = admin_webtest_client.get(url)
    response.form['name'] = 'New Name'
    response.form['description'] = 'New Description'

    form_response = response.form.submit()
    assert form_response.status_code == 302

    role = models.Role.objects.get(name='New Name')
    assert role.name == 'New Name'
    assert role.description == 'New Description'
    assert role.department == department
