from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomAdmin)
