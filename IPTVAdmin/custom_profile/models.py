from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth.models import User

from IPTVAdmin.core.models import AbstractBaseModel


class Profile(AbstractBaseModel):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfils'
        ordering = ['user__first_name', '-created_at']
        permissions = [
            ('list_profile', 'Pode Listar Perfils'),
        ]

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='profile')
    
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username


auditlog.register(User)
auditlog.register(Profile)
