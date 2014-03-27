from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()


admin.site.register(User)
