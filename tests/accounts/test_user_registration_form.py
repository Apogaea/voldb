import pytest

from volunteer.apps.accounts.forms import (
    UserRegistrationForm,
)


def test_enforces_email_uniqueness(factories):
    user = factories.UserFactory(email='test@example.com')

    form = UserRegistrationForm({'email': user.email})

    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_email_normalized():
    upper_email = 'TEST@EXAMPLE.COM'
    lower_email = 'test@example.com'

    form = UserRegistrationForm({'email': upper_email})

    assert form.is_valid()
    assert form.cleaned_data['email'] == lower_email
