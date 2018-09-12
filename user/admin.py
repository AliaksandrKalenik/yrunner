from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

USER_MODEL = get_user_model()


@admin.register(USER_MODEL)
class UserModelAdmin(UserAdmin):
    pass
