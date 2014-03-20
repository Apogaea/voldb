import urllib
import time
import mock

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse

User = get_user_model()

from rest_framework import status

from accounts.factories import UserFactory
from accounts.utils import (
    generate_registration_token, reverse_registration_url,
    unsign_registration_token, REGISTRATION_TOKEN_MAX_AGE,
)


class LoginTest(TestCase):
    def test_good_credentials(self):
        user = UserFactory(password='secret')
        url = reverse("login")
        response = self.client.post(url, {
            'username': user.email, 'password': 'secret',
        })
        self.assertEquals(response.status_code, status.HTTP_302_FOUND)

    def test_bad_credentials(self):
        user = UserFactory(password='secret')
        url = reverse("login")
        response = self.client.post(url, {
            'username': user.email, 'password': 'badpassword',
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class LogoutTest(TestCase):
    def test_logout(self):
        user = UserFactory(password='secret')

        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))

        url = reverse('logout')

        response = self.client.get(url)

        self.assertContains(response, '', status_code=status.HTTP_302_FOUND)

    def test_anonymous_logout(self):
        url = reverse('logout')

        response = self.client.get(url)

        self.assertContains(response, '', status_code=status.HTTP_302_FOUND)


class TokenizedRegistrationUrlTest(TestCase):
    def test_url_generation(self):
        token = generate_registration_token('test@example.com')
        url = reverse_registration_url('test@example.com')

        self.assertIn(urllib.quote_plus(token), url)

    def test_unsigning_token(self):
        original_email = 'test@example.com'
        token = generate_registration_token(original_email)
        resulting_email = unsign_registration_token(token)

        self.assertEqual(original_email, resulting_email)


class RegistrationTest(TestCase):
    def test_registration_page_loading(self):
        url = reverse('register')

        response = self.client.get(url)

        self.assertContains(response, '', status_code=status.HTTP_200_OK)

    def test_registration_email(self):
        url = reverse('register')

        self.assertFalse(len(mail.outbox))
        response = self.client.post(url, {
            'email': 'test@example.com',
        })
        self.assertContains(response, '', status_code=status.HTTP_302_FOUND)
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_confirmation_page_with_expired_link(self):
        now = time.time()
        expire_time = now + REGISTRATION_TOKEN_MAX_AGE + 1
        url = reverse_registration_url('test@example.com')

        with mock.patch('time.time', return_value=expire_time):
            get_response = self.client.get(url)
        self.assertContains(get_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(get_response.context['signature_expired'])

        with mock.patch('time.time', return_value=expire_time):
            post_response = self.client.post(url, {
                'password1': 'secret',
                'password2': 'secret',
            })
        self.assertContains(post_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(post_response.context['signature_expired'])

    def test_registration_confirmation_page_with_bad_token(self):
        url = reverse('register_confirm', kwargs={'token': 'BADTOKEN'})
        get_response = self.client.get(url)
        self.assertContains(get_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(get_response.context['bad_signature'])

        post_response = self.client.post(url, {
            'password1': 'secret',
            'password2': 'secret',
        })
        self.assertContains(post_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(post_response.context['bad_signature'])

    def test_registration_confirmation_page_with_email_taken(self):
        UserFactory(email='test@example.com')
        url = reverse_registration_url('test@example.com')

        get_response = self.client.get(url)
        self.assertContains(get_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(get_response.context['email_already_registered'])

        post_response = self.client.post(url, {
            'password1': 'secret',
            'password2': 'secret',
        })
        self.assertContains(post_response, '', status_code=status.HTTP_200_OK)
        self.assertTrue(post_response.context['email_already_registered'])

    def test_registration_confirmation_page(self):
        url = reverse_registration_url('test@example.com')

        response = self.client.get(url)
        self.assertContains(response, '', status_code=status.HTTP_200_OK)

    def test_registration_confirmation_submission(self):
        email = 'test@example.com'
        url = reverse_registration_url(email)

        response = self.client.post(url, {
            'password1': 'secret',
            'password2': 'secret',
        })
        self.assertContains(response, '', status_code=status.HTTP_302_FOUND)

        self.assertTrue(User.objects.filter(email=email).exists())

        user = User.objects.get(email='test@example.com')

        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('secret'))
        self.assertTrue(self.client.login(
            username=user.email,
            password='secret',
        ))
