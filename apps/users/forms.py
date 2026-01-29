"""
Forms for user registration.
"""
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users.
    """
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
