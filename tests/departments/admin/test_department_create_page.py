from django.core.urlresolvers import reverse


def test_department_create_page(admin_webtest_client, factories):
    url = reverse('admin:department-create')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_department_creation(admin_webtest_client, factories, models):
    assert not models.Department.objects.filter(name='New Name').exists()
    url = reverse('admin:department-create')

    response = admin_webtest_client.get(url)
    response.forms[1]['name'] = 'New Name'
    response.forms[1]['description'] = 'New Description'

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    department = models.Department.objects.get(name='New Name')
    assert department.name == 'New Name'
    assert department.description == 'New Description'
