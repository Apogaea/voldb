import urllib

from volunteer.apps.accounts.utils import (
    generate_registration_token,
    reverse_registration_url,
    unsign_registration_token,
)


def test_url_generation():
    token = generate_registration_token('test@example.com')
    url = reverse_registration_url('test@example.com')

    assert urllib.quote_plus(token) in url


def test_unsigning_token():
    original_email = 'test@example.com'
    token = generate_registration_token(original_email)
    resulting_email = unsign_registration_token(token)

    assert original_email == resulting_email
