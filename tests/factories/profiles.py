import factory

from volunteer.apps.profiles.models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('tests.factories.accounts.UserFactory')

    full_name = factory.Sequence('test-full_name-{0}'.format)
    display_name = factory.Sequence('test-display_name-{0}'.format)
    phone = factory.Sequence(lambda i: '555-555-{0}'.format(str(i).zfill(4)))
    has_ticket = True

    class Meta:
        model = Profile
        django_get_or_create = ("user",)
