from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

import factory

from accounts.models import create_volunteer_profile


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = factory.Sequence(lambda i: 'test-{0}@example.com'.format(i))

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_volunteer_profile, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_volunteer_profile, User)
        return user


class UserWithProfileFactory(UserFactory):
    _profile = factory.RelatedFactory('profiles.tests.factories.ProfileFactory', 'user')
