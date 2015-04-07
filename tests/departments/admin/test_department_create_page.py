from django.core.urlresolvers import reverse


def test_department_create_page(admin_webtest_client, factories):
    url = reverse('admin:department-create')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_department_creation(admin_webtest_client, factories, models):
    assert not models.Department.objects.filter(name='New Name').exists()
    url = reverse('admin:department-create')

    response = admin_webtest_client.get(url)
    response.form['name'] = 'New Name'
    response.form['description'] = 'New Description'

    form_response = response.form.submit()
    assert form_response.status_code == 302

    department = models.Department.objects.get(name='New Name')
    assert department.name == 'New Name'
    assert department.description == 'New Description'
