import time

from django.core import mail
from django.core.urlresolvers import reverse

from rest_framework import status

from volunteer.apps.accounts.utils import (
    generate_registration_token, reverse_registration_url,
    unsign_registration_token, REGISTRATION_TOKEN_MAX_AGE,
)


#
# Initiating Registration
#
def test_registration_page_loading(webtest_client):
    url = reverse('register')
    response = webtest_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_registration_page_for_logged_in_user(user_webtest_client):
    url = reverse('register')
    response = user_webtest_client.get(url)

    expected_location = reverse('dashboard')
    assert response.status_code == status.HTTP_302_FOUND
    assert response.location.endswith(expected_location)


def test_registration_email_is_sent(webtest_client):
    url = reverse('register')
    response = webtest_client.get(url)

    assert not len(mail.outbox)

    response.form['email'] = 'test@example.com'

    expected_location = reverse('register-success')
    register_response = response.form.submit()
    assert register_response.status_code == status.HTTP_302_FOUND
    assert register_response.location.endswith(expected_location)

    assert len(mail.outbox) == 1


#
# Confirmation Page
#
def test_registration_confirmation_page(webtest_client):
    url = reverse_registration_url('test@example.com')

    response = webtest_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_registration_confirmation_page_with_expired_link(client, mocker):
    now = time.time()
    expire_time = now + REGISTRATION_TOKEN_MAX_AGE + 1
    url = reverse_registration_url('test@example.com')

    with mocker.patch('time.time', return_value=expire_time):
        get_response = client.get(url)

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.context['signature_expired']

    with mocker.patch('time.time', return_value=expire_time):
        post_response = client.post(url)

    assert post_response.status_code == status.HTTP_200_OK
    assert post_response.context['signature_expired']


def test_registration_confirmation_page_with_bad_token(client):
    url = reverse('register-confirm', kwargs={'token': 'BADTOKEN'})
    get_response = client.get(url)

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.context['bad_signature']

    post_response = client.post(url)

    assert post_response.status_code == status.HTTP_200_OK
    assert post_response.context['bad_signature']


def test_registration_confirmation_page_email_token_that_is_already_registered(user, client):
    url = reverse_registration_url(user.email)

    get_response = client.get(url)
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.context['email_already_registered']

    post_response = client.post(url)

    assert post_response.status_code == status.HTTP_200_OK
    assert post_response.context['email_already_registered']


def test_registration_confirmation_submission(webtest_client, User):
    email = 'test@example.com'
    url = reverse_registration_url(email)

    response = webtest_client.get(url)

    response.form['password1'] = 'secret'
    response.form['display_name'] = 'test-display_name'
    response.form['full_name'] = 'test-full_name'
    response.form['phone'] = 'test-phone'
    response.form['has_ticket'] = True

    assert not User.objects.filter(email__iexact=email).exists()

    register_response = response.form.submit()

    expected_location = reverse('dashboard')
    assert register_response.status_code == status.HTTP_302_FOUND
    assert register_response.location.endswith(expected_location)

    assert User.objects.filter(email=email).exists()

    user = User.objects.get(email=email)

    assert user.is_active
    assert user.check_password('secret')

    assert user.profile.full_name == 'test-full_name'
    assert user.profile.display_name == 'test-display_name'
    assert user.profile.phone == 'test-phone'
    assert user.profile.has_ticket
