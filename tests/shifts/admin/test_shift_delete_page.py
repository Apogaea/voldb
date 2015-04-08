from django.core.urlresolvers import reverse


def test_shift_delete_page(admin_webtest_client, factories):
    shift = factories.ShiftFactory()
    url = reverse('admin:shift-delete', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_shift_deletion_is_protected_if_claimed_slots(admin_client, factories, models):
    shift = factories.ShiftFactory(num_slots=1, code='test')
    url = reverse('admin:shift-delete', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    factories.ShiftSlotFactory(shift=shift)
    assert shift.claimed_slots.exists()

    response = admin_client.post(url)
    assert response.status_code == 200

    assert models.Shift.objects.filter(pk=shift.pk).exists()


def test_shift_deletion(admin_client, factories, models):
    shift = factories.ShiftFactory(num_slots=1, code='test')
    url = reverse('admin:shift-delete', kwargs={
        'department_pk': shift.role.department_id,
        'role_pk': shift.role_id,
        'pk': shift.pk,
    })
    shift_slot = factories.ShiftSlotFactory(shift=shift)
    shift_slot.is_cancelled = True
    shift_slot.save()
    assert not shift.claimed_slots.exists()

    response = admin_client.post(url)
    assert response.status_code == 302

    assert not models.Shift.objects.filter(pk=shift.pk).exists()
