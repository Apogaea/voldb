from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'full_name', 'phone')

admin.site.register(Profile, ProfileAdmin)
