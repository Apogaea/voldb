from emailtools import (
    MarkdownEmail,
)
from emailtools.cbe import mixins

from volunteer.apps.accounts.utils import reverse_registration_url


class RegistrationVerificationEmail(mixins.BuildAbsoluteURIMixin, MarkdownEmail):
    template_name = 'registration/mail/email_verification.md'
    subject = 'Welcome to the Apogaea Volunteer Database'

    def __init__(self, email):
        self.to = email

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationVerificationEmail, self).get_context_data(**kwargs)
        kwargs.update({
            'confirm_email_url': self.build_absolute_uri(
                reverse_registration_url(self.to),
            ),
        })
        return kwargs

send_registration_verification_email = RegistrationVerificationEmail.as_callable()
