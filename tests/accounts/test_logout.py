from django.core.urlresolvers import reverse

from rest_framework import status


def test_logout(user_webtest_client):
    # sanity check that we are in fact logged in
    assert user_webtest_client.get(reverse('dashboard')).status_code == status.HTTP_200_OK

    url = reverse('logout')
    response = user_webtest_client.get(url)

    expected_location = reverse('login')
    assert response.status_code == status.HTTP_302_FOUND
    assert response.location.endswith(expected_location)


def test_anonymous_logout(webtest_client):
    url = reverse('logout')
    response = webtest_client.get(url)

    expected_location = reverse('login')
    assert response.status_code == status.HTTP_302_FOUND
    assert response.location.endswith(expected_location)
