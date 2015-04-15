from django.core.urlresolvers import reverse

from rest_framework import status


def test_profile_display(user_webtest_client, user):
    user.profile.display_name = 'test-display-name'
    user.profile.full_name = 'test-full-name'
    user.profile.phone = '555-444-1234'
    user.profile.save()

    response = user_webtest_client.get(reverse('dashboard'))
    assert response.status_code == status.HTTP_200_OK

    assert user.profile.full_name in response.content
    assert user.profile.display_name in response.content
    assert user.profile.phone in response.content
