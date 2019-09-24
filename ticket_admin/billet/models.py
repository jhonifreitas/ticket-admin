from auditlog.registry import auditlog

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ticket_admin.billet.manager import BilletManager
from ticket_admin.core.models import AbstractBaseModel
from ticket_admin.custom_profile.models import Profile


class Billet(AbstractBaseModel):

    class Meta:
        verbose_name = 'Boleto'
        verbose_name_plural = 'Boletos'
        ordering = ['-dueDate', '-created_at']
        permissions = [
            ('list_billet', 'Pode Listar Boletos'),
        ]

    objects = BilletManager()

    WAITING = '1'
    IN_ANALYSIS = '2'
    PAID = '3'
    DISPONIBLE = '4'
    IN_DISPUTE = '5'
    RETURNED = '6'
    CANCELED = '7'
    DEBITED = '8'
    TEMPORARY_RETENTION = '9'

    STATUS = [
        (WAITING, 'Aguardando pagamento'),
        (IN_ANALYSIS, 'Em análise'),
        (PAID, 'Pago'),
        (DISPONIBLE, 'Disponível'),
        (IN_DISPUTE, 'Em disputa'),
        (RETURNED, 'Devolvido'),
        (CANCELED, 'Cancelado'),
        (DEBITED, 'Debitado'),
        (TEMPORARY_RETENTION, 'Retenção temporária'),
    ]

    profile = models.ForeignKey(Profile, verbose_name='Perfil', on_delete=models.CASCADE, related_name='billets')

    code = models.CharField(verbose_name='Código', max_length=255, unique=True)
    paymentLink = models.URLField(verbose_name='Link de Pagamento')
    barcode = models.CharField(verbose_name='Código de Barras', max_length=255, null=True, blank=True)
    dueDate = models.DateField(verbose_name='Vencimento', null=True, blank=True)

    reference = models.CharField(verbose_name='Referencia', max_length=200)
    numberOfPayments = models.PositiveIntegerField(verbose_name='Períodos mensais', validators=[
        MinValueValidator(1), MaxValueValidator(12)], default=1)
    instructions = models.CharField(verbose_name='Instruções', max_length=100)
    description = models.CharField(verbose_name='Descrição', max_length=100)
    status = models.CharField(verbose_name='Status', choices=STATUS, default=WAITING, max_length=255)
    amount = models.DecimalField(verbose_name='Valor', max_digits=15, decimal_places=2)

    def __str__(self):
        return self.code


auditlog.register(Billet)
