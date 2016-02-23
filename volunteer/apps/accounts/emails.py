import ogmios

from volunteer.apps.accounts.utils import reverse_registration_url


def build_absolute_uri(location, domain=None, protocol="http"):
    if domain is None:
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain

    current_uri = '{protocol}://{domain}{location}'.format(
        protocol=protocol,
        domain=domain,
        location=location,
    )
    return current_uri


def send_registration_verification_email(to):
    ogmios.send_email(
        'registration/mail/email_verification.md',
        {
            'confirm_email_url': build_absolute_uri(reverse_registration_url(to)),
            'to': to,
        },
    )
