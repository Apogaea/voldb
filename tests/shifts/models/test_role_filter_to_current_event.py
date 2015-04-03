def test_filters_roles_without_current_shifts(factories, models):
    old_event = factories.PastEventFactory()
    current_event = factories.EventFactory()

    role_a = factories.RoleFactory()
    role_b = factories.RoleFactory()

    factories.ShiftFactory(event=old_event, role=role_b)

    factories.ShiftFactory(event=old_event, role=role_a)
    factories.ShiftFactory(event=current_event, role=role_a)

    assert role_a in models.Role.objects.filter_to_current_event()
    assert role_b not in models.Role.objects.filter_to_current_event()
