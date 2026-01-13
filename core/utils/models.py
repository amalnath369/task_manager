from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    """Base model with common fields"""
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not self.pk and not self.created_by_id:
            # Try to get current user from thread local
            from crum import get_current_user
            user = get_current_user()
            if user and isinstance(user, User):
                self.created_by = user
        
        # Always update updated_by
        from crum import get_current_user
        user = get_current_user()
        if user and isinstance(user, User):
            self.updated_by = user
        
        super().save(*args, **kwargs)