from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from betterforms.forms import BetterForm, BetterModelForm

from profiles.models import Profile


class UserRegistrationForm(BetterForm):
    email = forms.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email__iexact=value)
        except User.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(
                'An account with that email address already exists',
            )


class UserRegistrationConfirmForm(BetterModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    full_name = forms.CharField(required=False)
    display_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    has_ticket = forms.BooleanField(label='I have a ticket', required=False)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above,"
                                " for verification.")

    class Meta:
        model = User
        fields = tuple()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationConfirmForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(BetterModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'display_name', 'phone', 'has_ticket')
