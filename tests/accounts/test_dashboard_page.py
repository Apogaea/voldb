from django.core.urlresolvers import reverse

from rest_framework import status


def test_profile_display(user_webtest_client, user):
    response = user_webtest_client.get(reverse('dashboard'))

    assert response.status_code == status.HTTP_200_OK

    assert user.profile.full_name in response.content
    assert user.profile.display_name in response.content
    assert user.profile.phone in response.content
