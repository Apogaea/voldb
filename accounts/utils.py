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
