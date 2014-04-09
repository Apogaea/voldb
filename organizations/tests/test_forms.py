from django.test import TestCase

from organizations.forms import OrganizationCreateForm, MembershipRequestForm
from organizations.models import (
    MembershipRequest, Membership,
)
from organizations.tests.factories import (
    OrganizationFactory, MembershipRequestFactory,
)


class OrganizationCreateFormTest(TestCase):
    def test_name_collision(self):
        organization = OrganizationFactory()

        form = OrganizationCreateForm({'name': organization.name})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_alternately_cased_name_collision(self):
        organization = OrganizationFactory()

        self.assertNotEqual(organization.name, organization.name.upper())

        form = OrganizationCreateForm({'name': organization.name.upper()})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class MembershipReqestFormTest(TestCase):
    def test_confirmation(self):
        request = MembershipRequestFactory()

        form = MembershipRequestForm({
            'accept_or_reject': MembershipRequestForm.ACCEPT_CHOICE,
        }, instance=request)
        self.assertTrue(form.is_valid())

        confirmed_request = form.save()

        self.assertIsInstance(confirmed_request, Membership)
        self.assertTrue(Membership.objects.filter(pk=request.pk).exists())

    def test_rejection(self):
        request = MembershipRequestFactory()

        form = MembershipRequestForm({
            'accept_or_reject': MembershipRequestForm.REJECT_CHOICE,
        }, instance=request)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertFalse(MembershipRequest.objects.filter(pk=request.pk).exists())

    def test_no_choice(self):
        request = MembershipRequestFactory()

        form = MembershipRequestForm({}, instance=request)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertTrue(MembershipRequest.objects.filter(pk=request.pk).exists())
        self.assertFalse(Membership.objects.filter(pk=request.pk).exists())
