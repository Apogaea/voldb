from django.core import signing
from django.views.generic import FormView, CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, login as auth_login, authenticate

User = get_user_model()

from accounts.forms import (
    UserRegistrationForm, UserRegistrationConfirmForm,
)
from accounts.emails import send_registration_verification_email
from accounts.utils import unsign_registration_token


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        send_registration_verification_email(form.data['email'])
        return super(RegisterView, self).form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'registration/register_success.html'


class RegisterConfirmView(CreateView):
    template_name = 'registration/register_confirm.html'
    model = User
    form_class = UserRegistrationConfirmForm
    success_url = reverse_lazy('grid')  # TODO, where should users get redirected post registration?

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
        form.instance.email = self.email
        password = form.data['password1']
        form.save()
        user = authenticate(
            username=form.instance.email,
            password=password,
        )
        auth_login(self.request, user)
        return redirect(self.success_url)
