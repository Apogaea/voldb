from django.core.urlresolvers import reverse

from rest_framework import status


def test_edit_page_loading(user_webtest_client):
    url = reverse('profile-edit')
    response = user_webtest_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_editing(user_webtest_client, models, user):
    url = reverse('profile-edit')
    response = user_webtest_client.get(url)

    user.profile.has_ticket = False
    user.profile.save()

    response.forms[1]['full_name'] = 'updated-full_name'
    response.forms[1]['display_name'] = 'updated-display_name'
    response.forms[1]['phone'] = 'updated-phone'
    response.forms[1]['has_ticket'] = True

    form_response = response.forms[1].submit()

    expected_target = reverse('dashboard')
    assert form_response.status_code == status.HTTP_302_FOUND
    assert form_response.location.endswith(expected_target)

    profile = models.Profile.objects.get(pk=user.profile.pk)

    assert profile.full_name == 'updated-full_name'
    assert profile.display_name == 'updated-display_name'
    assert profile.phone == 'updated-phone'
    assert profile.has_ticket
