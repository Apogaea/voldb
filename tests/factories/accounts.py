import factory

from volunteer.apps.accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence('test-{0}@example.com'.format)

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    _profile = factory.RelatedFactory('tests.factories.profiles.ProfileFactory', factory_related_name="user")

    class Meta:
        model = User
