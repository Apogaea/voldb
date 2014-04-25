from django.test import TestCase
from django.core import signing
from django.core.validators import validate_email
from django.core.urlresolvers import reverse

REGISTRATION_SALT = 'registration'
REGISTRATION_TOKEN_MAX_AGE = 60 * 60 * 24 * 2  # 2 days


def generate_registration_token(email):
    return signing.dumps(email, salt=REGISTRATION_SALT)


def reverse_registration_url(email):
    validate_email(email)
    token = generate_registration_token(email)
    return reverse('register_confirm', kwargs={'token': token})


def unsign_registration_token(token):
    return signing.loads(
        token, salt=REGISTRATION_SALT, max_age=REGISTRATION_TOKEN_MAX_AGE,
    )


def obfuscate_string(value, filler='*', index=1, min_length=4):
    left = value[:index]
    right = filler * max(len(value[index:]), min_length - 1)
    return left + right


def obfuscate_email(email):
    left, _, right = email.partition('@')
    if not right:
        return obfuscate_string(left)
    if len(left) > 3:
        return '@'.join([
            obfuscate_string(left),
            right,
        ])
    else:
        domain, _, tld = right.partition('.')
        return '{left}@{domain}.{tld}'.format(
            left=obfuscate_string(left),
            domain=obfuscate_string(domain),
            tld=tld,
        )


class AuthenticatedTestCase(TestCase):
    def setUp(self):
        from accounts.factories import UserWithProfileFactory
        super(AuthenticatedTestCase, self).setUp()
        self.user = UserWithProfileFactory(password='secret')

        self.assertTrue(self.client.login(
            username=self.user.email,
            password='secret',
        ))
