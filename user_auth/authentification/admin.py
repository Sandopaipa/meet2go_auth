from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .froms import UserCreationForm, UserChangeForm


admin.site.register(User)