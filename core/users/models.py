from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import BaseModel


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    admin = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_users',
        limit_choices_to={'role__in': ['ADMIN', 'SUPERADMIN']}
    )
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_superadmin(self):
        return self.role == 'SUPERADMIN'
    
    @property
    def is_admin(self):
        return self.role in ['ADMIN', 'SUPERADMIN']
    
    @property
    def is_regular_user(self):
        return self.role == 'USER'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']