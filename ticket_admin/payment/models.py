from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth.models import User

from ticket_admin.storage import get_storage_path
from ticket_admin.core.models import AbstractBaseModel


def get_file_path(instance, filename):
    return get_storage_path(filename, 'payment')


class Payment(AbstractBaseModel):

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']
        permissions = [
            ('list_payment', 'Pode Listar Pagamentos'),
        ]

    IN_ANALYZE = 'in_analyze'
    APPROVED = 'approved'
    NOT_APPROVED = 'not_approved'

    STATUS = [
        (APPROVED, 'Aprovado'),
        (IN_ANALYZE, 'Em análise'),
        (NOT_APPROVED, 'Não aprovado')
    ]

    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='payments')
    image = models.ImageField(verbose_name='Imagem', upload_to=get_file_path)
    date = models.DateField(verbose_name='Data')
    status = models.CharField(verbose_name='Status', max_length=255, choices=STATUS, default=IN_ANALYZE)
    message = models.TextField(verbose_name='Mensagem', null=True, blank=True)


auditlog.register(Payment)
