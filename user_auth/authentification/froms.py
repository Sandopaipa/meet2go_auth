from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


BASE_FIELD_SET = (
    'email',
    'password',
    'first_name',
    'last_name',
    'birthdate'
)
class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = BASE_FIELD_SET


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = BASE_FIELD_SET