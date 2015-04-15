from django.core.urlresolvers import reverse

from rest_framework import status


def test_public_profile_display(user_webtest_client, user, factories):
    other_user = factories.UserFactory()

    response = user_webtest_client.get(reverse('public-profile', kwargs={'pk': other_user.pk}))
    assert response.status_code == status.HTTP_200_OK

    assert other_user.display_name in response.content
