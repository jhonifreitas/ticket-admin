from auditlog.registry import auditlog

from django.db import models

from IPTVAdmin.core.models import AbstractBaseModel, Config


class Profile(AbstractBaseModel):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfils'
        ordering = ['name', '-created_at']
        permissions = [
            ('list_profile', 'Pode Listar Perfils'),
        ]

    config = models.ForeignKey(Config, verbose_name='Configuração', on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(verbose_name='Nome', max_length=255)
    phone = models.CharField(verbose_name='Telefone', max_length=11)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return self.name


auditlog.register(Profile)
