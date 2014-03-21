from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'id', 'user', 'full_name')
    list_filter = ['user', 'camps']

admin.site.register(Profile, ProfileAdmin)
