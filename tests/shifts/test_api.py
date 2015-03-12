from django.core.urlresolvers import reverse

from rest_framework import status


def test_claim_endpoint_requires_authentication(client, factories):
    shift = factories.ShiftFactory()
    url = reverse('shift-detail', kwargs={'pk': shift.pk})

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.data
