from django import template

register = template.Library()


@register.filter('get_color_status')
def get_color_status(value):
    color = 'dark'
    # if Indication.PENDING == value:
    #     color = 'warning'
    # elif Indication.NOT_ACTIVE == value:
    #     color = 'danger'
    # elif Indication.ACTIVE == value:
    #     color = 'success'
    return color


@register.filter('mask_phone')
def mask_phone(value):
    if len(value) == 10:
        return '({}) {}-{}'.format(value[0:2], value[2:6], value[6:])
    elif len(value) == 11:
        return '({}) {}-{}'.format(value[0:2], value[2:7], value[7:])
    return '---'


@register.filter('concat')
def concat(value, concat):
    return str(value) + str(concat)
