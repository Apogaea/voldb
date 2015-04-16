from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django import forms

from betterforms.forms import (
    BetterForm,
    BetterModelForm,
)


User = get_user_model()


class AdminUserChangeForm(BetterModelForm):
    full_name = forms.CharField(required=False)
    display_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    has_ticket = forms.BooleanField(label='I have a ticket', required=False)

    class Meta:
        model = User
        fields = (
            "is_active",
            "is_staff",
            "email",
            "full_name",
            "display_name",
            "phone",
            "has_ticket",
        )

    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        initial = kwargs.get('initial', {})
        initial.setdefault('display_name', instance.profile.display_name)
        initial.setdefault('full_name', instance.profile.full_name)
        initial.setdefault('phone', instance.profile.phone)
        initial.setdefault('has_ticket', instance.profile.has_ticket)
        super(AdminUserChangeForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with that email address already exists',
            )
        return email

    def save(self, *args):
        user = super(AdminUserChangeForm, self).save(*args)
        user.profile.full_name = self.cleaned_data['full_name']
        user.profile.display_name = self.cleaned_data['display_name']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.has_ticket = self.cleaned_data['has_ticket']
        user.profile.save()
        return user


class AdminUserSearchForm(BetterForm):
    q = forms.CharField(validators=[MinLengthValidator(3)], required=False)
