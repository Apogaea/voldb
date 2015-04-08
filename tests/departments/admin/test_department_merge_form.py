from volunteer.apps.departments.admin.forms import AdminDepartmentMergeForm


def test_verify_field_validation_with_bad_value(factories):
    department_a = factories.DepartmentFactory(name='a')
    department_b = factories.DepartmentFactory(name='b')

    form = AdminDepartmentMergeForm(instance=department_a, data={
        'department': department_b.pk,
        'verify': 'not-the-right-name',
    })
    assert not form.is_valid()
    assert 'verify' in form.errors


def test_verify_field_validation_with_correct_value(factories):
    department_a = factories.DepartmentFactory(name='a')
    department_b = factories.DepartmentFactory(name='b')

    form = AdminDepartmentMergeForm(instance=department_a, data={
        'department': department_b.pk,
        'verify': department_a.name,
    })
    assert form.is_valid(), form.errors


def test_merging_with_other_department(factories, models):
    department_a = factories.DepartmentFactory(name='a')
    department_b = factories.DepartmentFactory(name='b')

    form = AdminDepartmentMergeForm(instance=department_a, data={
        'department': department_b.pk,
        'verify': department_a.name,
    })
    assert form.is_valid(), form.errors
    form.save()

    assert not models.Department.objects.filter(pk=department_a.pk).exists()
