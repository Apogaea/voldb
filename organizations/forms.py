from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from betterforms.forms import BetterModelForm

from organizations.models import Organization, MembershipRequest, Membership


class OrganizationCreateForm(BetterModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'is_closed')

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            Organization.objects.get(name__iexact=name)
        except Organization.DoesNotExist:
            return name
        else:
            raise forms.ValidationError(
                'An organization with that name already exists.',
            )


class OrganizationUpdateForm(BetterModelForm):
    class Meta:
        model = Organization
        fields = ('is_closed',)


class BaseMembershipFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BaseMembershipFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.exclude(user=self.user)
        self.max_num = self.queryset.count()


MembershipFormSet = inlineformset_factory(
    Organization,
    Membership,
    formset=BaseMembershipFormSet,
    fields=('is_admin',),
    extra=0,
)


class BaseMembershipRequestFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseMembershipRequestFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.not_confirmed()
        self.max_num = self.queryset.count()


class MembershipRequestForm(BetterModelForm):
    ACCEPT_CHOICE = 'accept'
    REJECT_CHOICE = 'reject'
    ACCEPT_OR_REJECT_CHOICES = (
        ('', 'No Choice'),
        (ACCEPT_CHOICE, 'Accept'),
        (REJECT_CHOICE, 'Reject'),
    )
    accept_or_reject = forms.ChoiceField(
        choices=ACCEPT_OR_REJECT_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    class Meta:
        model = MembershipRequest
        fields = tuple()

    def clean(self):
        try:
            Membership.objects.get(pk=self.instance.pk)
        except Membership.DoesNotExist:
            return super(MembershipRequestForm, self).clean()
        else:
            raise forms.ValidationError('This request has already been accepted')

    def save(self, commit=True):
        assert commit
        if self.cleaned_data['accept_or_reject'] == self.ACCEPT_CHOICE:
            # promote
            membership = Membership(membershiprequest_ptr=self.instance)
            membership.__dict__.update(self.instance.__dict__)
            self.instance = membership
        elif self.cleaned_data['accept_or_reject'] == self.REJECT_CHOICE:
            self.instance.delete()
            return self.instance
        return super(MembershipRequestForm, self).save()


MembershipRequestFormSet = inlineformset_factory(
    Organization,
    MembershipRequest,
    formset=BaseMembershipRequestFormSet,
    form=MembershipRequestForm,
    can_delete=False,
    extra=0,
)
