import factory

from organizations.models import Organization, MembershipRequest, Membership


class OrganizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Organization
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = 'Fucking Unicorns'
    is_closed = False

    @factory.post_generation
    def admins(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for admin in extracted:
                membership, created = self.users.through.objects.get_or_create(
                    user=admin,
                    organization=self,
                    defaults={'is_admin': True},
                )
                if created:
                    membership.is_admin = True
                    membership.save()

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for member in extracted:
                membership, created = self.users.through.objects.get_or_create(
                    user=member,
                    organization=self,
                )


class MembershipRequestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MembershipRequest

    user = factory.SubFactory('accounts.factories.UserWithProfileFactory')
    organization = factory.SubFactory('organizations.tests.factories.OrganizationFactory')


class MembershipFactory(MembershipRequestFactory):
    FACTORY_FOR = Membership

    is_admin = False
