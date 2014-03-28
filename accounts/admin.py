from django.contrib.auth import get_user_model
from django.contrib import admin
from accounts.models import User

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'date_joined')
    list_filter = ['user_permissions', 'date_joined']

admin.site.register(User, UserAdmin)
