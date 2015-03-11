import factory

from accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda i: 'test-{0}@example.com'.format(i))

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    class Meta:
        model = User
