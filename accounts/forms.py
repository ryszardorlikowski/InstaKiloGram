from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'profile_image', 'email', 'first_name', 'password1', 'password2')
