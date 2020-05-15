from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth.models import User

from ticket_admin.core.models import AbstractBaseModel


class Panel(AbstractBaseModel):

    class Meta:
        verbose_name = 'Painel'
        verbose_name_plural = 'Painéis'
        ordering = ['name', '-created_at']
        permissions = [
            ('list_panel', 'Pode Listar Painéis'),
        ]

    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='panels')
    name = models.CharField(verbose_name='Nome', max_length=255)
    value = models.DecimalField(verbose_name='Valor do crédito', max_digits=11, decimal_places=2)


auditlog.register(Panel)
