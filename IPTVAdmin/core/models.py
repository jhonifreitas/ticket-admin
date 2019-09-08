from uuid import uuid4

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from IPTVAdmin.core.manager import Manager
from IPTVAdmin.core.signals import post_soft_delete


class AbstractBaseModel(models.Model):

    class Meta:
        abstract = True

    history = AuditlogHistoryField()
    uuid = models.UUIDField(verbose_name='UUID', default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(verbose_name=_('Deleted at'), null=True, blank=True)
    objects = Manager()
    objects_all = models.Manager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
        post_soft_delete.send(sender=type(self), instance=self, using=self._state.db)

    def __str__(self):
        return str(self.pk)


class Config(AbstractBaseModel):

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configuração'

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='config')
    token = models.CharField(verbose_name='Token', max_length=255)
    instructions_billet = models.CharField(verbose_name='Instruções', max_length=100)
    description_billet = models.CharField(verbose_name='Descrição', max_length=100)
    amount_billet = models.DecimalField(verbose_name='Valor', max_digits=15, decimal_places=2)


auditlog.register(User)
auditlog.register(Config)
