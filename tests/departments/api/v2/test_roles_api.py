from django.core.urlresolvers import reverse


def test_shifts_api_endpoint(factories, api_client):
    factories.RoleFactory.create_batch(30)

    list_url = reverse('v2:role-list')

    response = api_client.get(list_url)

    assert response.status_code == 200, response.data
    assert response.data.get('results')
