from datetime import datetime, timedelta

from django import template

from ticket_admin.billet.models import Billet
from ticket_admin.payment.models import Payment
from ticket_admin.custom_profile.models import ProfileUser

register = template.Library()


@register.filter('get_billet_color_status')
def get_billet_color_status(value):
    color = 'dark'
    if Billet.WAITING == value:
        color = 'warning'
    elif Billet.CANCELED == value:
        color = 'danger'
    elif Billet.PAID == value or Billet.DEBITED == value:
        color = 'success'
    return color


@register.filter('get_payment_color_status')
def get_payment_color_status(value):
    color = 'dark'
    if Payment.IN_ANALYZE == value:
        color = 'warning'
    elif Payment.NOT_APPROVED == value:
        color = 'danger'
    elif Payment.APPROVED == value:
        color = 'success'
    return color


@register.filter('get_user_color_status')
def get_user_color_status(user):
    color = 'dark'
    status = user.status
    ten = datetime.now().date() + timedelta(days=10)

    if user.expiration < datetime.now().date():
        status = ProfileUser.EXPIRED
        user.status = status
        user.save()
    elif user.expiration <= ten:
        status = ProfileUser.WAITING
        user.status = status
        user.save()
    else:
        status = ProfileUser.ACTIVE
        user.status = status
        user.save()

    if ProfileUser.WAITING == status:
        color = 'warning'
    elif ProfileUser.EXPIRED == status:
        color = 'danger'
    elif ProfileUser.ACTIVE == status:
        color = 'success'
    elif ProfileUser.IN_TEST == status:
        color = 'orange'
    return color


@register.filter('get_whats_message')
def get_whats_message(user):
    message = 'Olá!%0a'
    message += 'Seu sinal irá vencer dia *{}*%0a'.format(user.expiration.strftime('%d/%m/%Y'))
    message += 'O valor do pagamento é de *R$ {}*%0a'.format(str(user.value).replace('.', ','))
    message += 'Por favor, renove antes do corte de sinal.%0a%0a'
    if user.profile.user.banks.count():
        message += '*Bancos para Depósito/Transferência*%0a'
        for bank in user.profile.user.banks.all():
            message += '*{}*%0a'.format(bank.name)
            message += 'Agência: {}%0a'.format(bank.agency)
            message += 'Conta: {}%0a'.format(bank.account)
            message += '{}%0a'.format(bank.get_types_display())
            if bank.operation:
                message += 'Operação: {}%0a'.format(bank.operation)
            message += '{}%0a'.format(bank.fullname)
            message += 'CPF: {}'.format(bank.get_cpf_formated)
    return message
