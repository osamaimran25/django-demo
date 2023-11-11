from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Setting username as None

    # Set email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    # Add any other fields that should be required
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email