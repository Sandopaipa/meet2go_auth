from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .froms import UserCreationForm, UserChangeForm


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        'username',
        'first_name',
        'last_name',
        'birthdate'
    )

admin.site.register(User, UserAdmin)