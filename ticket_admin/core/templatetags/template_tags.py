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
    elif user.expiration <= ten:
        status = ProfileUser.WAITING
    else:
        status = ProfileUser.ACTIVE

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
    if ProfileUser.EXPIRED == user.status:
        message += 'Seu sinal venceu dia *{}*%0a'.format(user.expiration.strftime('%d/%m/%Y'))
        message += 'O valor do pagamento é de *R$ {}*%0a'.format(str(user.value).replace('.', ','))
        message += 'Por favor, efetue o pagamento o volte a usar os canais.'
    else:
        message += 'Seu sinal irá vencer dia *{}*%0a'.format(user.expiration.strftime('%d/%m/%Y'))
        message += 'O valor do pagamento é de *R$ {}*%0a'.format(str(user.value).replace('.', ','))
        message += 'Por favor, evite o corte de sinal.'

    if user.profile.user.banks.count():
        message += '%0a%0a*Bancos para Depósito/Transferência*'
        for i, bank in enumerate(user.profile.user.banks.all()):
            if i != 0:
                message += '%0a'
            message += '%0a*{}*%0a'.format(bank.name)
            message += '{}%0a'.format(bank.fullname)
            if bank.pix:
                message += 'Pix: {}%0a'.format(bank.pix)
            if bank.agency:
                message += 'Agência: {}%0a'.format(bank.agency)
            if bank.account:
                message += 'Conta: {}%0a'.format(bank.account)
            if bank.types:
                message += '{}%0a'.format(bank.get_types_display())
            if bank.operation:
                message += 'Operação: {}%0a'.format(bank.operation)
            if bank.cpf:
                message += 'CPF: {}'.format(bank.get_cpf_formated)
    return message
