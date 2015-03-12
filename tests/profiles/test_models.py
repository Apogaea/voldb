from django.test import TestCase
from django.contrib.auth import get_user_model

from volunteer.apps.profiles.models import Profile

User = get_user_model()


class ProfileCreationTest(TestCase):
    def test_profile_created_for_new_user(self):
        self.assertFalse(Profile.objects.exists())

        user = User.objects.create(email='test@example.com')

        self.assertTrue(Profile.objects.exists())
        self.assertTrue(user.profile)
