from django.core.urlresolvers import reverse


def test_role_merge_page(admin_webtest_client, factories):
    role = factories.RoleFactory()
    url = reverse('admin:role-merge', kwargs={
        'department_pk': role.department_id,
        'pk': role.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_role_merging(admin_webtest_client, factories, models):
    role_a = factories.RoleFactory(name='a')
    factories.ShiftFactory(role=role_a)
    role_b = factories.RoleFactory(name='b')
    factories.ShiftFactory(role=role_b)

    assert role_a != role_b

    # sanity check
    assert role_a.shifts.count() == 1
    assert role_b.shifts.count() == 1

    url = reverse('admin:role-merge', kwargs={
        'department_pk': role_a.department_id,
        'pk': role_a.pk,
    })

    response = admin_webtest_client.get(url)
    response.forms[1]['role'] = role_b.pk
    response.forms[1]['verify'] = role_a.name

    form_response = response.forms[1].submit()
    assert form_response.status_code == 302

    assert not models.Role.objects.filter(pk=role_a.pk).exists()
    assert role_b.shifts.count() == 2
