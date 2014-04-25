from django.test import TestCase

from accounts.forms import UserRegistrationForm
from accounts.factories import UserWithProfileFactory


class RegistrationFormTest(TestCase):
    def test_enforces_email_uniqueness(self):
        user = UserWithProfileFactory(email='test@example.com')

        form = UserRegistrationForm({'email': user.email})

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_normalized(self):
        upper_email = 'TEST@EXAMPLE.COM'
        lower_email = 'test@example.com'

        form = UserRegistrationForm({'email': upper_email})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], lower_email)
