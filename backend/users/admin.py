from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UsersAdmin(UserAdmin):

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    search_fields = ('username', 'email')
