from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from tests.factories.accounts import UserFactory
from volunteer.apps.profiles.models import Profile

User = get_user_model()


class ProfileEditingTest(TestCase):
    def setUp(self):
        super(ProfileEditingTest, self).setUp()

        self.user = UserFactory(password='secret')
        self.profile = self.user.profile

        self.profile.full_name = 'test-full_name'
        self.profile.display_name = 'test-display_name'
        self.profile.phone = 'test-phone'
        self.profile.has_ticket = False
        self.profile.save()

        self.assertTrue(self.client.login(
            username=self.user.email,
            password='secret',
        ))

    def test_profile_display(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(self.profile.full_name, response.content)
        self.assertIn(self.profile.display_name, response.content)
        self.assertIn(self.profile.phone, response.content)

    def test_editing(self):
        response = self.client.post(reverse('profile_edit'), {
            'full_name': 'updated-full_name',
            'display_name': 'updated-display_name',
            'phone': 'updated-phone',
            'has_ticket': True,
        })

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.full_name, 'updated-full_name')
        self.assertEqual(profile.display_name, 'updated-display_name')
        self.assertEqual(profile.phone, 'updated-phone')
        self.assertTrue(profile.has_ticket)


class ChangePasswordTest(TestCase):
    def setUp(self):
        super(ChangePasswordTest, self).setUp()

        self.user = UserFactory(password='secret')
        self.assertTrue(self.client.login(
            username=self.user.email,
            password='secret',
        ))
        self.url = reverse('password_change')

    def test_page_load(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        response = self.client.post(self.url, {
            'old_password': 'secret',
            'new_password1': 'new-secret',
            'new_password2': 'new-secret',
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password('new-secret'))
