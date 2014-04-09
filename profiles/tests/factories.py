import factory

from profiles.models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Profile

    user = factory.SubFactory('accounts.factories.UserFactory')

    full_name = factory.Sequence(lambda i: 'Test User-{0}'.format(i))
    display_name = factory.Sequence(lambda i: 'User-{0}'.format(i))
    phone = factory.Sequence(lambda i: '555-555-{0}'.format(str(i).zfill(4)))
