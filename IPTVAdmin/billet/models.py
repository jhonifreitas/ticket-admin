from auditlog.registry import auditlog

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from IPTVAdmin.core.models import AbstractBaseModel
from IPTVAdmin.custom_profile.models import Profile


class Billet(AbstractBaseModel):

    class Meta:
        verbose_name = 'Boleto'
        verbose_name_plural = 'Boletos'
        permissions = [
            ('list_billet', 'Pode Listar Boletos'),
        ]
    
    PENDING = 'pending'
    APPROVED = 'approved'
    RECUSED = 'recused'
    
    STATUS = [
        (PENDING, 'Pendente'),
        (APPROVED, 'Aprovado'),
        (RECUSED, 'Recusado'),
    ]

    profile = models.ForeignKey(Profile, verbose_name='Perfil', on_delete=models.CASCADE, related_name='billets')
    
    code = models.CharField(verbose_name='Código', max_length=255, unique=True)
    paymentLink = models.URLField(verbose_name='Link de Pagamento')
    barcode = models.CharField(verbose_name='Código de Barras', max_length=255)
    dueDate = models.DateField(verbose_name='Vencimento')

    reference = models.CharField(verbose_name='Referencia', max_length=200)
    firstDueDate = models.DateField(verbose_name='Data de vencimento')
    numberOfPayments = models.PositiveIntegerField(verbose_name='Parcelas', validators=[
        MinValueValidator(1), MaxValueValidator(12)], default=1)
    instructions = models.CharField(verbose_name='Instruções', max_length=100)
    description = models.CharField(verbose_name='Descrição', max_length=100)
    status = models.CharField(verbose_name='Status', choices=STATUS, default=PENDING, max_length=255)
    amount = models.DecimalField(verbose_name='Valor', max_digits=15, decimal_places=2)
    
    def __str__(self):
        return self.profile


auditlog.register(Billet)
