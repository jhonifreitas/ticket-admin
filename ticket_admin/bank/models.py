from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth.models import User

from ticket_admin.core.utils import CPF
from ticket_admin.core.models import AbstractBaseModel


class Bank(AbstractBaseModel):

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['name', '-created_at']
        permissions = [
            ('list_bank', 'Pode Listar Bancos'),
        ]

    CC = 'cc'
    CP = 'cp'

    TYPES = [
        (CC, 'Conta-corrente'),
        (CP, 'Conta-poupança')
    ]

    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='banks')
    name = models.CharField(verbose_name='Nome do banco', max_length=255)
    agency = models.CharField(verbose_name='Agencia', max_length=255)
    account = models.CharField(verbose_name='Conta com digito', max_length=255)
    fullname = models.CharField(verbose_name='Nome Completo', max_length=255)
    types = models.CharField(verbose_name='Tipo', max_length=255, choices=TYPES)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    operation = models.CharField(verbose_name='Operação', max_length=255, null=True, blank=True)

    @property
    def get_cpf_formated(self):
        return CPF(self.cpf).format()


auditlog.register(Bank)
