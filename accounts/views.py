from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    model = User
    success_url = reverse_lazy('home')
