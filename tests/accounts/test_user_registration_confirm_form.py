from volunteer.apps.accounts.forms import (
    UserRegistrationConfirmForm,
)


def test_form_checks_display_name_uniqueness(user):
    user.profile.display_name = 'test_name'
    user.profile.save()

    form = UserRegistrationConfirmForm({
        'display_name': 'test_name',
    })

    assert not form.is_valid()
    assert 'display_name' in form.errors
