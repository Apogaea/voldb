from django.core.urlresolvers import reverse

from shifts.api.v2.serializers import ShiftSerializer


def test_shifts_list_api_endpoint(factories, api_client):
    factories.ShiftFactory.create_batch(30)

    list_url = reverse('v2:shift-list')

    response = api_client.get(list_url)

    assert response.status_code == 200, response.data
    assert response.data.get('results')

# Read from the detail endpoint
# That I can update an unclaimed shift.
# That I am not allowed to update a shift claimed by someone else.
# That I am allowed to update shifts claimed by me.
def test_shifts_detail_api_endpoint(factories, api_client):
    shift = factories.ShiftFactory()

    detail_url = reverse('v2:shift-detail', kwargs={'pk': shift.pk})

    response = api_client.get(detail_url)

    assert response.status_code == 200, response.data
    assert response.data['id'] == shift.id


def test_claiming_a_shift(factories, api_client, models):
    shift = factories.ShiftFactory(owner=None)
    assert shift.owner is None

    shift_data = ShiftSerializer(shift).data
    shift_data['owner'] = api_client.user.pk

    detail_url = reverse('v2:shift-detail', kwargs={'pk': shift.pk})

    response = api_client.put(detail_url, shift_data)

    assert response.status_code == 200, response.data
    assert response.data['id'] == shift.id
    assert response.data['owner'] == api_client.user.pk

    updated_shift = models.Shift.objects.get(pk=shift.pk)
    assert updated_shift.owner == api_client.user


def test_releasing_own_shift(factories, api_client, models):
    shift = factories.ShiftFactory(owner=api_client.user)

    shift_data = ShiftSerializer(shift).data
    shift_data['owner'] = None

    detail_url = reverse('v2:shift-detail', kwargs={'pk': shift.pk})

    response = api_client.put(detail_url, shift_data)

    assert response.status_code == 200, response.data
    assert response.data['id'] == shift.id
    assert response.data['owner'] is None

    updated_shift = models.Shift.objects.get(pk=shift.pk)
    assert updated_shift.owner is None


def test_cannot_releasing_others_shift(factories, api_client, models):
    other_user = factories.UserFactory()
    shift = factories.ShiftFactory(owner=other_user)

    shift_data = ShiftSerializer(shift).data
    shift_data['owner'] = api_client.user.pk

    detail_url = reverse('v2:shift-detail', kwargs={'pk': shift.pk})

    response = api_client.put(detail_url, shift_data)

    assert response.status_code == 400, response.data
