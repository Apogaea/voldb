from django.forms.models import modelform_factory
from django.views.generic import (
    DetailView, ListView, CreateView, UpdateView,
)
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse

from authtools.views import LoginRequiredMixin

from organizations.models import (
    Organization, MembershipRequest, Membership,
)
from organizations.forms import (
    OrganizationCreateForm, OrganizationUpdateForm, MembershipFormSet,
    MembershipRequestFormSet, MyMembershipFormSet,
)


class OrganizationListView(ListView):
    template_name = 'organizations/organization_list.html'
    model = Organization
    context_object_name = 'organization_list'


class OrganizationDetailView(DetailView):
    template_name = 'organizations/organization_detail.html'
    model = Organization
    context_object_name = 'organization'


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'organizations/organization_create.html'
    model = Organization
    form_class = OrganizationCreateForm

    def form_valid(self, form):
        self.object = organization = form.save()
        Membership.objects.get_or_create(
            user=self.request.user,
            organization=organization,
            defaults={'is_admin': True},
        )
        return redirect(self.get_success_url())


class OrganizationAdminRequiredMixin(LoginRequiredMixin):
    def get_object(self):
        membership = get_object_or_404(
            Membership,
            organization__pk=self.kwargs['pk'],
            user=self.request.user,
            is_admin=True,
        )
        return membership.organization


class OrganizationUpdateView(OrganizationAdminRequiredMixin, UpdateView):
    template_name = 'organizations/organization_update.html'
    model = Organization
    form_class = OrganizationUpdateForm


class OrganizationManageMembersView(OrganizationAdminRequiredMixin, UpdateView):
    template_name = 'organizations/organization_membership.html'
    model = Organization
    form_class = MembershipFormSet

    def get_form_kwargs(self):
        kwargs = super(OrganizationManageMembersView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = self.get_object()
        self.object_list = form.save()
        return redirect(self.get_success_url())


class OrganizationManageRequestsView(OrganizationAdminRequiredMixin, UpdateView):
    template_name = 'organizations/organization_requests.html'
    model = Organization
    form_class = MembershipRequestFormSet

    def form_valid(self, form):
        self.object = self.get_object()
        self.object_list = form.save()
        return redirect(self.get_success_url())


class OrganizationJoinView(LoginRequiredMixin, UpdateView):
    template_name = 'organizations/organization_join.html'
    model = Organization
    context_object_name = 'organization'
    form_class = modelform_factory(Organization, fields=tuple())

    def dispatch(self, *args, **kwargs):
        organization = self.get_object()
        if self.request.user in organization.members:
            return redirect(organization.get_absolute_url())
        return super(OrganizationJoinView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        organization = form.instance
        user = self.request.user

        if organization.is_closed:
            membership, _ = MembershipRequest.objects.get_or_create(
                user=user,
                organization=organization,
            )
            return redirect(reverse('organization_join_success', kwargs={
                'pk': organization.pk,
            }))
        else:
            membership, _ = Membership.objects.get_or_create(
                user=user,
                organization=organization,
            )
            return redirect(organization.get_absolute_url())


class OrganizationJoinSuccessView(LoginRequiredMixin, DetailView):
    template_name = 'organizations/organization_join_success.html'
    model = Organization
    context_object_name = 'organization'


class MyOrganizationMembershipView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/my_organizations.html'
    form_class = MyMembershipFormSet

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        self.object = self.get_object()
        self.object_list = form.save()
        return redirect(self.get_success_url())
