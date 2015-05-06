from django.core.urlresolvers import reverse


def test_department_add_lead_page(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    url = reverse('admin:department-lead-add', kwargs={'pk': department.pk})
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_adding_lead_to_department(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    user = factories.UserFactory()
    url = reverse('admin:department-lead-add', kwargs={'pk': department.pk})

    assert not department.leads.exists()

    response = admin_webtest_client.get(url)
    response.form['user'] = user.pk

    form_response = response.form.submit()
    assert form_response.status_code == 302

    assert department.leads.filter(pk=user.pk).exists()


def test_department_remove_lead_page(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    user = factories.UserFactory()
    department.leads.add(user)

    url = reverse('admin:department-lead-remove', kwargs={
        'pk': department.pk,
        'lead_pk': user.pk,
    })

    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_removing_lead_from_department(admin_webtest_client, factories):
    department = factories.DepartmentFactory()
    user = factories.UserFactory()
    department.leads.add(user)

    url = reverse('admin:department-lead-remove', kwargs={
        'pk': department.pk,
        'lead_pk': user.pk,
    })

    response = admin_webtest_client.get(url)
    form_response = response.form.submit()

    assert form_response.status_code == 302
    assert not department.leads.exists()
