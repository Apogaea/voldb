from django.core import signing
from django.views.generic import (
    FormView,
    CreateView,
    TemplateView,
    DetailView,
    UpdateView,
)
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import (
    get_user_model,
    login as auth_login,
    authenticate,
)

from authtools.views import LoginRequiredMixin

from volunteer.apps.shifts.utils import group_shifts

from volunteer.apps.accounts.forms import (
    UserRegistrationForm,
    UserRegistrationConfirmForm,
    ProfileForm,
)
from volunteer.apps.accounts.emails import send_registration_verification_email
from volunteer.apps.accounts.utils import unsign_registration_token

User = get_user_model()


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_success')

    def form_valid(self, form):
        send_registration_verification_email(form.cleaned_data['email'])
        return super(RegisterView, self).form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'registration/register_success.html'


class RegisterConfirmView(CreateView):
    template_name = 'registration/register_confirm.html'
    model = User
    form_class = UserRegistrationConfirmForm
    success_url = reverse_lazy('shifts')

    def dispatch(self, *args, **kwargs):
        try:
            self.email = self.get_email_from_token()
        except signing.SignatureExpired:
            return self.render_to_response({'signature_expired': True})
        except signing.BadSignature:
            return self.render_to_response({'bad_signature': True})
        else:
            if User.objects.filter(email__iexact=self.email).exists():
                return self.render_to_response({
                    'email_already_registered': True,
                    'email': self.email,
                })
            return super(RegisterConfirmView, self).dispatch(*args, **kwargs)

    def get_email_from_token(self):
        return unsign_registration_token(self.kwargs['token'])

    def get_context_data(self, **kwargs):
        kwargs = super(RegisterConfirmView, self).get_context_data(**kwargs)
        kwargs.update({
            'token': self.kwargs['token'],
            'email': self.email,
        })
        return kwargs

    def form_valid(self, form):
        form.instance.email = self.email.lower()
        password = form.cleaned_data['password1']
        form.save()
        # profile fields
        profile = form.instance.profile
        profile.display_name = form.cleaned_data['display_name']
        profile.full_name = form.cleaned_data['full_name']
        profile.phone = form.cleaned_data['phone']
        profile.has_ticket = form.cleaned_data['has_ticket']
        profile.save()
        # authenticate
        user = authenticate(
            username=form.instance.email,
            password=password,
        )
        auth_login(self.request, user)
        return redirect(self.success_url)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['grouped_shifts'] = group_shifts(self.object.shifts.all())
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
