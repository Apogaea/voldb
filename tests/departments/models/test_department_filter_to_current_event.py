def test_filters_department_to_ones_with_active_shifts_for_current_event(factories, models):
    old_event = factories.PastEventFactory()
    current_event = factories.EventFactory()

    department_a = factories.DepartmentFactory(name='dept-a')
    department_b = factories.DepartmentFactory(name='dept-b')

    role_a = factories.RoleFactory(department=department_a)
    role_b = factories.RoleFactory(department=department_b)

    factories.ShiftFactory(event=old_event, role=role_b)

    factories.ShiftFactory(event=old_event, role=role_a)
    factories.ShiftFactory(event=current_event, role=role_a)

    assert department_a in models.Department.objects.filter_to_current_event()
    assert department_b not in models.Department.objects.filter_to_current_event()
