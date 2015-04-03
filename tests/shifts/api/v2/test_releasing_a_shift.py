from django.core.urlresolvers import reverse

from rest_framework import status


def test_canceling_own_shift(factories, api_client, models, user):
    shift_slot = factories.ShiftSlotFactory(volunteer=user)
    url = reverse("v2:shiftslot-detail", kwargs={"pk": shift_slot.pk})

    assert not shift_slot.is_cancelled

    response = api_client.put(url, {'is_cancelled': True})
    assert response.status_code == status.HTTP_200_OK, response.data

    updated_slot = models.ShiftSlot.objects.get(pk=shift_slot.pk)
    assert updated_slot.is_cancelled


def test_canceling_others_shift(factories, api_client, models, user):
    shift_slot = factories.ShiftSlotFactory()
    assert shift_slot.volunteer != user
    url = reverse("v2:shiftslot-detail", kwargs={"pk": shift_slot.pk})

    assert not shift_slot.is_cancelled

    response = api_client.put(url, {'is_cancelled': True})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    updated_slot = models.ShiftSlot.objects.get(pk=shift_slot.pk)
    assert not updated_slot.is_cancelled
