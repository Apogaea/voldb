from django.core.urlresolvers import reverse


def test_department_list_page(admin_webtest_client, factories):
    factories.DepartmentFactory.create_batch(2)
    url = reverse('admin:department-list')
    response = admin_webtest_client.get(url)
    assert response.status_code == 200
