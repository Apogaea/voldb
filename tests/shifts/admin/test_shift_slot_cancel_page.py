from django.core.urlresolvers import reverse


def test_shift_slot_cancel_page(admin_webtest_client, factories):
    shift_slot = factories.ShiftSlotFactory()
    url = reverse('admin:shift-slot-cancel', kwargs={
        'department_pk': shift_slot.shift.role.department_id,
        'role_pk': shift_slot.shift.role_id,
        'shift_pk': shift_slot.shift.pk,
        'pk': shift_slot.pk,
    })
    response = admin_webtest_client.get(url)
    assert response.status_code == 200


def test_shift_slot_cancelling(admin_webtest_client, factories, models):
    shift_slot = factories.ShiftSlotFactory()
    url = reverse('admin:shift-slot-cancel', kwargs={
        'department_pk': shift_slot.shift.role.department_id,
        'role_pk': shift_slot.shift.role_id,
        'shift_pk': shift_slot.shift.pk,
        'pk': shift_slot.pk,
    })

    response = admin_webtest_client.get(url)
    form_response = response.form.submit()
    assert form_response.status_code == 302

    updated_shift_slot = models.ShiftSlot.objects.get(pk=shift_slot.pk)
    assert updated_shift_slot.is_cancelled
