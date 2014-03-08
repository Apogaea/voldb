from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


class AuthTest(TestCase):
    def test_good_credentials(self):
        user = User.objects.create(email="test@example.com")
        user.set_password("test")
        user.save()
        url = reverse("login")
        response = self.client.post(url, {
            'username': user.email, 'password': 'test',
        })
        self.assertEquals(response.status_code, 302)

    def test_bad_credentials(self):
        user = User.objects.create(email="test@example.com")
        user.set_password("test")
        user.save()
        url = reverse("login")
        response = self.client.post(url, {
            'username': user.email, 'password': 'badpassword',
        })
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        user = User.objects.create(email="test@example.com")
        user.set_password("test")
        user.save()
        self.client.login(username=user.email, password="test")
        self.assertIn('_auth_user_id', self.client.session)
        self.client.post(reverse("logout"))
        self.assertNotIn('_auth_user_id', self.client.session)
