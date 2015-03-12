from django.contrib.auth import get_user_model
from django.contrib import admin
from profiles.models import Profile


User = get_user_model()


class ProfileInLine(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'date_joined', '__unicode__')
    list_filter = ['email', 'date_joined']
    inlines = [ProfileInLine, ]

admin.site.register(User, UserAdmin)
