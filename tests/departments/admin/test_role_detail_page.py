from django.core.urlresolvers import reverse


def test_role_detail_page(admin_webtest_client, factories):
    role = factories.RoleFactory()
    url = reverse('admin:role-detail', kwargs={
        'department_pk': role.department_id,
        'pk': role.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_role_editing(admin_webtest_client, factories, models):
    role = factories.RoleFactory()
    url = reverse('admin:role-detail', kwargs={
        'department_pk': role.department_id,
        'pk': role.pk,
    })

    response = admin_webtest_client.get(url)
    response.forms[1]['name'] = 'New Name'
    response.forms[1]['description'] = 'New Description'

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    updated_role = models.Role.objects.get(pk=role.pk)
    assert updated_role.name == 'New Name'
    assert updated_role.description == 'New Description'
