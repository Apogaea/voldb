from django.test import TestCase

from accounts.factories import UserWithProfileFactory

from shifts.factories import ShiftFactory

from organizations.models import MembershipRequest
from organizations.tests.factories import (
    OrganizationFactory, MembershipRequestFactory, MembershipFactory,
)


class TotalMemberShiftHoursTest(TestCase):
    def test_no_members(self):
        organization = OrganizationFactory()
        self.assertEqual(organization.total_member_shift_hours, 0)

    def test_with_shifts(self):
        # 2 shifts for user_a
        user_a = UserWithProfileFactory()
        ShiftFactory(owner=user_a, shift_length=3)
        ShiftFactory(owner=user_a, shift_length=5)

        # 1 shift for user_b
        user_b = UserWithProfileFactory()
        ShiftFactory(owner=user_b, shift_length=7)

        # no shifts for user_c
        user_c = UserWithProfileFactory()

        organization = OrganizationFactory(members=[user_a, user_b, user_c])

        self.assertEqual(organization.total_member_shift_hours, 15)


class AdminMembersTest(TestCase):
    def test_admin_membership(self):
        user_a = UserWithProfileFactory()
        user_b = UserWithProfileFactory()
        user_c = UserWithProfileFactory()

        organization_a = OrganizationFactory(
            name='Fucking Unicorns',
            admins=[user_a],
            members=[user_b, user_c],
        )
        organization_b = OrganizationFactory(
            name='Narwhals',
            admins=[user_a, user_b],
            members=[user_c],
        )

        self.assertIn(user_a, organization_a.members)
        self.assertIn(user_a, organization_a.admin_members)

        self.assertIn(user_b, organization_a.members)
        self.assertNotIn(user_b, organization_a.admin_members)

        self.assertIn(user_c, organization_a.members)
        self.assertNotIn(user_c, organization_a.admin_members)

        self.assertIn(user_a, organization_b.members)
        self.assertIn(user_a, organization_b.admin_members)

        self.assertIn(user_b, organization_b.members)
        self.assertIn(user_b, organization_b.admin_members)

        self.assertIn(user_c, organization_b.members)
        self.assertNotIn(user_c, organization_b.admin_members)

    def test_normal_membership(self):
        organization = OrganizationFactory()
        user = UserWithProfileFactory()

        MembershipFactory(organization=organization, user=user)

        self.assertIn(user, organization.members)

    def test_requesting_user_is_not_in_members(self):
        organization = OrganizationFactory()
        user = UserWithProfileFactory()

        MembershipRequestFactory(organization=organization, user=user)

        self.assertNotIn(user, organization.members)


class MembershipRequestNotConfirmedTest(TestCase):
    def test_not_confirmed_queryset_method(self):
        membership_request = MembershipRequestFactory()
        membership = MembershipFactory()

        self.assertIn(membership_request, MembershipRequest.objects.not_confirmed())
        self.assertNotIn(membership, MembershipRequest.objects.not_confirmed())
