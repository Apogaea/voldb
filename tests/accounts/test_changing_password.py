from django.core.urlresolvers import reverse

from rest_framework import status


def test_page_load(user, user_webtest_client):
    url = reverse('password-change')
    response = user_webtest_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_change_password(user_webtest_client, User, user):
    url = reverse('password-change')
    response = user_webtest_client.get(url)

    response.forms[1]['old_password'] = 'password'
    response.forms[1]['new_password1'] = 'new-password'
    response.forms[1]['new_password2'] = 'new-password'

    expected_location = reverse('dashboard')
    form_response = response.forms[1].submit()
    assert form_response.status_code == status.HTTP_302_FOUND
    assert form_response.location.endswith(expected_location)

    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.check_password('new-password')
