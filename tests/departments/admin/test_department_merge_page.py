from django.core.urlresolvers import reverse


def test_department_merge_page(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    url = reverse('admin:department-merge', kwargs={'pk': department.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_department_merging(admin_webtest_client, factories, models):
    department_a = factories.DepartmentFactory(name='a')
    factories.RoleFactory(department=department_a)
    department_b = factories.DepartmentFactory(name='b')
    factories.RoleFactory(department=department_b)

    assert department_a != department_b

    # sanity check
    assert department_a.roles.count() == 1
    assert department_b.roles.count() == 1

    url = reverse('admin:department-merge', kwargs={'pk': department_a.pk})

    response = admin_webtest_client.get(url)
    response.forms[1]['department'] = department_b.pk
    response.forms[1]['verify'] = department_a.name

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    assert not models.Department.objects.filter(pk=department_a.pk).exists()
    assert department_b.roles.count() == 2
