from django.contrib import admin
from accounts.models import User

 
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'date_joined')
    list_filter = ['user_permissions', 'date_joined']

admin.site.register(User, UserAdmin)