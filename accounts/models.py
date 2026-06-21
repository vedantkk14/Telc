from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICE = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher')
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICE
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField( auto_now_add=True )

    updated_at = models.DateTimeField( auto_now=True )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email