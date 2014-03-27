from django.views.generic import DetailView,ListView
from accounts.models import User
from profiles.models import Profile
import pprint


class ProfileView(DetailView):
    queryset = Profile.objects.all()
    template_name = "profiles/profile.html"

    def get_object(self):
        # Call the superclass
        profile = super(ProfileView, self).get_object()
        # Update the user
        return profile

class ProfilesView(ListView):
    queryset = Profile.objects.all()
    template_name = "profiles/profiles.html"

    def get_queryset(self):
        qs = super(ProfilesView, self).get_queryset()
        return qs.select_related()

    def get_context_data(self, **kwargs):
        context = super(ProfilesView, self).get_context_data(**kwargs)
        pprint.pprint(context)
        return context        
