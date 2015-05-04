from django.core.urlresolvers import reverse


def test_assign_user_to_shift_page(admin_webtest_client, factories):
    shift = factories.ShiftFactory()
    url = reverse('admin:shift-slot-create', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_assigning_a_user(admin_webtest_client, factories, models):
    shift = factories.ShiftFactory()
    user = factories.UserFactory()
    url = reverse('admin:shift-slot-create', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    response = admin_webtest_client.get(url)

    assert not models.ShiftSlot.objects.filter(volunteer=user).exists()

    response.form['volunteer'] = user.pk
    form_response = response.form.submit()
    assert form_response.status_code == 302

    assert models.ShiftSlot.objects.filter(volunteer=user).exists()
    assert shift.slots.exists()


def test_assigning_a_user_who_is_already_volunteered(admin_webtest_client,
                                                     factories, models):
    shift = factories.ShiftFactory()
    user = factories.UserFactory()
    factories.ShiftSlotFactory(shift=shift, volunteer=user)

    url = reverse('admin:shift-slot-create', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    response = admin_webtest_client.get(url)

    assert models.ShiftSlot.objects.filter(volunteer=user).count() == 1

    response.form['volunteer'] = user.pk
    form_response = response.form.submit()
    assert form_response.status_code == 200

    assert models.ShiftSlot.objects.filter(volunteer=user).count() == 1
