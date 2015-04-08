from volunteer.apps.departments.admin.forms import AdminRoleMergeForm


def test_verify_field_validation_with_bad_value(factories):
    role_a = factories.RoleFactory(name='a')
    role_b = factories.RoleFactory(name='b')

    form = AdminRoleMergeForm(instance=role_a, data={
        'role': role_b.pk,
        'verify': 'not-the-right-name',
    })
    assert not form.is_valid()
    assert 'verify' in form.errors


def test_verify_field_validation_with_correct_value(factories):
    role_a = factories.RoleFactory(name='a')
    role_b = factories.RoleFactory(name='b')

    form = AdminRoleMergeForm(instance=role_a, data={
        'role': role_b.pk,
        'verify': role_a.name,
    })
    assert form.is_valid(), form.errors


def test_merging_with_other_role(factories, models):
    role_a = factories.RoleFactory(name='a')
    role_b = factories.RoleFactory(name='b')

    form = AdminRoleMergeForm(instance=role_a, data={
        'role': role_b.pk,
        'verify': role_a.name,
    })
    assert form.is_valid(), form.errors
    form.save()

    assert not models.Role.objects.filter(pk=role_a.pk).exists()
