from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    class Role(models.TextChoices):
        ADMIN  = 'admin',  'Admin'
        CLIENT = 'client', 'Client'

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='company'
    )
    company_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=64, unique=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name
