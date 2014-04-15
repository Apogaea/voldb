from django.contrib.auth import get_user_model
from django.contrib import admin
from accounts.models import User
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name')

admin.site.register(Profile, ProfileAdmin)
