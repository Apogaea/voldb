from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status

from accounts.factories import UserFactory
from accounts.utils import AuthenticatedTestCase

from organizations.forms import MembershipRequestForm
from organizations.models import Organization, MembershipRequest, Membership
from organizations.tests.factories import (
    OrganizationFactory, MembershipRequestFactory, MembershipFactory,
)


class OrganizationViewingTest(TestCase):
    def test_organization_list_page(self):
        unicorns = OrganizationFactory(name='Fucking Unicorns')
        narwhals = OrganizationFactory(name='Fucking Narwhals')

        url = reverse('organization_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(unicorns, response.context['organization_list'])
        self.assertIn(narwhals, response.context['organization_list'])

    def test_organization_detail_page(self):
        organization = OrganizationFactory()
        url = organization.get_absolute_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrganizationCreationTest(AuthenticatedTestCase):
    def setUp(self):
        super(OrganizationCreationTest, self).setUp()
        self.url = reverse('organization_create')

    def test_organization_creation_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_an_organization(self):
        response = self.client.post(self.url, {
            'name': 'Fucking Unicorns',
            'is_closed': True,
        })

        self.assertTrue(Organization.objects.filter(
            name='Fucking Unicorns',
        ).exists())

        organization = Organization.objects.get(name='Fucking Unicorns')

        self.assertRedirects(response, organization.get_absolute_url())


class OrganizationUpdateViewTest(AuthenticatedTestCase):
    def setUp(self):
        super(OrganizationUpdateViewTest, self).setUp()
        self.organization = OrganizationFactory()
        self.url = reverse('organization_update', kwargs={
            'pk': self.organization.pk,
        })

    def test_admin_member_allowed(self):
        MembershipFactory(user=self.user, organization=self.organization, is_admin=True)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_organization(self):
        MembershipFactory(user=self.user, organization=self.organization, is_admin=True)

        response = self.client.post(self.url, {
            'is_closed': not self.organization.is_closed,
        })

        self.assertRedirects(response, self.organization.get_absolute_url())

        updated_organization = Organization.objects.get(pk=self.organization.pk)
        self.assertNotEqual(updated_organization.is_closed, self.organization.is_closed)

    def test_normal_member_not_allowed(self):
        MembershipFactory(user=self.user, organization=self.organization, is_admin=False)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_member_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrganizationMemberManagementTest(AuthenticatedTestCase):
    def setUp(self):
        super(OrganizationMemberManagementTest, self).setUp()
        self.organization = OrganizationFactory(admins=[self.user])
        # Add one normal member
        MembershipFactory(organization=self.organization, user=UserFactory())
        # Add one other admin member
        MembershipFactory(organization=self.organization, user=UserFactory())
        self.url = reverse('organization_manage_members', kwargs={
            'pk': self.organization.pk,
        })

    def test_editing_user_not_included_in_formset(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotIn(self.user, response.context['form'].queryset)

    def test_changing_user_to_admin(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        formset = response.context['form']

        post_data = {
            'organization_membership-TOTAL_FORMS': formset.total_form_count(),
            'organization_membership-INITIAL_FORMS': formset.initial_form_count(),
            'organization_membership-MAX_NUM_FORMS': formset.max_num,
            'organization_membership-MIN_NUM_FORMS': formset.min_num,
        }

        # get the two forms
        membership_a_form, membership_b_form = [form for form in formset]

        # set the form ids
        post_data[membership_a_form['membershiprequest_ptr'].html_name] = membership_a_form['membershiprequest_ptr'].value()
        post_data[membership_b_form['membershiprequest_ptr'].html_name] = membership_b_form['membershiprequest_ptr'].value()

        # set the second member to not be an admin.
        post_data[membership_b_form['is_admin'].html_name] = True

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, self.organization.get_absolute_url())

        membership_b_pk = membership_b_form['membershiprequest_ptr'].value()

        membership_b = Membership.objects.get(pk=membership_b_pk)

        self.assertTrue(membership_b.is_admin)

    def test_deleting_a_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        formset = response.context['form']

        post_data = {
            'organization_membership-TOTAL_FORMS': formset.total_form_count(),
            'organization_membership-INITIAL_FORMS': formset.initial_form_count(),
            'organization_membership-MAX_NUM_FORMS': formset.max_num,
            'organization_membership-MIN_NUM_FORMS': formset.min_num,
        }

        # get the two forms
        membership_a_form, membership_b_form = [form for form in formset]

        # set the form ids
        post_data[membership_a_form['membershiprequest_ptr'].html_name] = membership_a_form['membershiprequest_ptr'].value()
        post_data[membership_b_form['membershiprequest_ptr'].html_name] = membership_b_form['membershiprequest_ptr'].value()

        # set the first member to be deleted.
        post_data[membership_a_form['DELETE'].html_name] = True

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, self.organization.get_absolute_url())

        membership_a_pk = membership_a_form['membershiprequest_ptr'].value()

        self.assertFalse(Membership.objects.filter(pk=membership_a_pk).exists())


class OrganizationJoiningViewTest(AuthenticatedTestCase):
    def setUp(self):
        super(OrganizationJoiningViewTest, self).setUp()
        self.organization = OrganizationFactory()
        self.url = reverse('organization_join', kwargs={
            'pk': self.organization.pk,
        })

    def test_join_organization_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_joining_an_open_organization(self):
        self.assertNotIn(self.user, self.organization.members)

        response = self.client.post(self.url)
        self.assertRedirects(response, self.organization.get_absolute_url())

        self.assertIn(self.user, self.organization.members)

    def test_joining_an_closed_organization(self):
        self.organization.is_closed = True
        self.organization.save()

        self.assertNotIn(self.user, self.organization.members)

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse(
            'organization_join_success',
            kwargs={'pk': self.organization.pk},
        ))

        self.assertNotIn(self.user, self.organization.members)


class OrganizationMembershipRequestTest(AuthenticatedTestCase):
    def setUp(self):
        super(OrganizationMembershipRequestTest, self).setUp()
        self.organization = OrganizationFactory(admins=[self.user])
        # Add one normal member
        MembershipRequestFactory(organization=self.organization, user=UserFactory())

        self.url = reverse('organization_manage_requests', kwargs={
            'pk': self.organization.pk
        })

    def test_accepting_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        formset = response.context['form']

        post_data = {
            'organization_membership-TOTAL_FORMS': formset.total_form_count(),
            'organization_membership-INITIAL_FORMS': formset.initial_form_count(),
            'organization_membership-MAX_NUM_FORMS': formset.max_num,
            'organization_membership-MIN_NUM_FORMS': formset.min_num,
        }

        # get the two forms
        membership_form = formset.forms[0]

        # set the form ids
        post_data[membership_form['id'].html_name] = membership_form['id'].value()

        # set the second member to not be an admin.
        post_data[membership_form['accept_or_reject'].html_name] = MembershipRequestForm.ACCEPT_CHOICE

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, self.organization.get_absolute_url())

        membership_pk = membership_form['id'].value()

        self.assertTrue(Membership.objects.filter(pk=membership_pk).exists())

    def test_rejecting_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        formset = response.context['form']

        post_data = {
            'organization_membership-TOTAL_FORMS': formset.total_form_count(),
            'organization_membership-INITIAL_FORMS': formset.initial_form_count(),
            'organization_membership-MAX_NUM_FORMS': formset.max_num,
            'organization_membership-MIN_NUM_FORMS': formset.min_num,
        }

        # get the two forms
        membership_form = formset.forms[0]

        # set the form ids
        post_data[membership_form['id'].html_name] = membership_form['id'].value()

        # set the second member to not be an admin.
        post_data[membership_form['accept_or_reject'].html_name] = MembershipRequestForm.REJECT_CHOICE

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, self.organization.get_absolute_url())

        membership_pk = membership_form['id'].value()

        self.assertFalse(Membership.objects.filter(pk=membership_pk).exists())
        self.assertFalse(MembershipRequest.objects.filter(pk=membership_pk).exists())
