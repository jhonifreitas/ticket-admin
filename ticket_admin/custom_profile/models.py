from auditlog.registry import auditlog

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from ticket_admin.core.utils import Phone
from ticket_admin.panel.models import Panel
from ticket_admin.core.models import AbstractBaseModel
from ticket_admin.custom_profile.manager import ProfileUserManager


class Profile(AbstractBaseModel):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfils'
        ordering = ['name', '-created_at']
        permissions = [
            ('list_profile', 'Pode Listar Perfils'),
        ]

    MONEY = 'active'
    BILLET = 'billet'
    TRANSFER = 'transfer'
    CREDIT_CARD = 'credit_card'

    PAY_METHOD = [
        (BILLET, 'Boleto'),
        (MONEY, 'Dinheiro'),
        (CREDIT_CARD, 'Cartão de Crédito'),
        (TRANSFER, 'Transferência bancária'),
    ]

    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(verbose_name='Nome', max_length=255, help_text='Nome e sobrenome')
    phone = models.CharField(verbose_name='Telefone', max_length=11)
    cpf = models.CharField(verbose_name='CPF', max_length=11, null=True, blank=True)
    pay_method = models.CharField(verbose_name='Forma de Pagamento', max_length=255, choices=PAY_METHOD,
                                  default=BILLET)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    observation = models.TextField(verbose_name='Observação', null=True, blank=True)

    @property
    def get_phone_formated(self):
        return Phone(self.phone).format()

    @property
    def get_total_amount(self):
        return ProfileUser.objects.filter(
            profile=self).values('profile').order_by('profile').annotate(total=Sum('value'))[0].get('total')


class ProfileUser(AbstractBaseModel):

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username', '-created_at']
        permissions = [
            ('list_profile_user', 'Pode Listar Usuários do Perfil'),
        ]

    objects = ProfileUserManager()

    ACTIVE = 'active'
    EXPIRED = 'expired'
    IN_TEST = 'in_test'
    WAITING = 'waiting_payment'

    STATUS = [
        (ACTIVE, 'Ativo'),
        (WAITING, 'Aguardando pagamento'),
        (EXPIRED, 'Vencido'),
        (IN_TEST, 'Em teste')
    ]

    profile = models.ForeignKey(Profile, verbose_name='Perfil', on_delete=models.CASCADE, related_name='users')
    panel = models.ForeignKey(Panel, verbose_name='Painel', on_delete=models.CASCADE, related_name='users')
    username = models.CharField(verbose_name='Usuário', max_length=255)
    password = models.CharField(verbose_name='Senha', max_length=255)
    value = models.DecimalField(verbose_name='Valor', max_digits=11, decimal_places=2)
    points = models.PositiveSmallIntegerField(verbose_name='Pontos', default=1)
    expiration = models.DateField(verbose_name='Expiração')
    status = models.CharField(verbose_name='Status', max_length=255, choices=STATUS, default=IN_TEST)
    observation = models.TextField(verbose_name='Observação', null=True, blank=True)


auditlog.register(Profile)
auditlog.register(ProfileUser)
