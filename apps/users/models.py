"""
User models for Coreano Marcial.
Custom User extending Django's AbstractUser.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Allows for future extensibility (e.g., profile picture, preferences).
    """
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.username
