from uuid import uuid4

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ticket_admin.core.manager import Manager
from ticket_admin.storage import get_storage_path
from ticket_admin.core.signals import post_soft_delete


def get_tutorial_file_path(instance, filename):
    return get_storage_path(filename, 'tutorial')


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
        if hasattr(self, 'name'):
            return self.name
        if hasattr(self, 'title'):
            return self.title
        return str(self.pk)


class Config(AbstractBaseModel):

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='config')
    token = models.CharField(verbose_name='Token', max_length=255)
    instructions_billet = models.CharField(verbose_name='Instruções', max_length=100)
    description_billet = models.CharField(verbose_name='Descrição', max_length=100)


class Tutorial(AbstractBaseModel):

    class Meta:
        verbose_name = 'Tutorial'
        verbose_name_plural = 'Tutoriais'
        ordering = ['order', 'name']
        permissions = [
            ('list_tutorial', 'Pode Listar Tutoriais'),
        ]

    name = models.CharField(verbose_name='Nome', max_length=255)
    url = models.URLField(verbose_name='Url', null=True, blank=True)
    order = models.PositiveSmallIntegerField(verbose_name='Ordem', default=0)


class TutorialImage(AbstractBaseModel):

    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    tutorial = models.ForeignKey(Tutorial, verbose_name='Tutorial', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Imagem', upload_to=get_tutorial_file_path)
    title = models.CharField(verbose_name='Título', max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)


auditlog.register(User)
auditlog.register(Config)
auditlog.register(Tutorial)
auditlog.register(TutorialImage)
