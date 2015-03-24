from django.core.urlresolvers import reverse

from rest_framework import status


def test_claiming_a_shift(factories, api_client, user):
    shift = factories.ShiftFactory()
    assert not shift.slots.exists()
    url = reverse("v2:shift-claim", kwargs={"pk": shift.pk})

    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert shift.slots.exists()

    slot = shift.slots.get()
    assert slot.volunteer == user


def test_that_an_unclaimable_shift_errors(factories, api_client, user):
    shift = factories.ShiftFactory(event=factories.PastEventFactory())
    assert not shift.is_claimable_by_user(user)
    url = reverse("v2:shift-claim", kwargs={"pk": shift.pk})

    response = api_client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not shift.slots.exists()
