from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import (
    urlsafe_base64_encode,
    default_token_generator,
)
from django.utils.encoding import force_bytes

from rest_framework import status


def test_page_load(user, webtest_client):
    url = reverse('password-reset')
    response = webtest_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_initiate_password_reset(webtest_client, User, user):
    url = reverse('password-reset')
    response = webtest_client.get(url)

    response.form['email'] = user.email

    assert len(mail.outbox) == 0

    expected_location = reverse('password-reset-done')
    form_response = response.form.submit()
    assert form_response.status_code == status.HTTP_302_FOUND
    assert form_response.location.endswith(expected_location)

    assert len(mail.outbox) == 1


def test_password_reset_confirm_page(client, factories, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.get(reverse(
        'password-reset-confirm-and-login',
        kwargs={
            'uidb64': uidb64,
            'token': token,
        },
    ))
    assert response.status_code == status.HTTP_200_OK
    assert response.context['validlink'] is True


def test_password_reset_confirming(webtest_client, factories, User, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse(
        'password-reset-confirm-and-login',
        kwargs={
            'uidb64': uidb64,
            'token': token,
        },
    )
    response = webtest_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response.form['new_password1'] = 'new-secret'
    response.form['new_password2'] = 'new-secret'

    expected_location = reverse('dashboard')
    reset_response = response.form.submit()

    assert reset_response.status_code == status.HTTP_302_FOUND
    assert reset_response.location.endswith(expected_location)

    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.check_password('new-secret')
