from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from auditlog.apps import AuditlogConfig
from django.utils.translation import ugettext_lazy as _


class AuditlogCustomConfig(AuditlogConfig):
    verbose_name = _('Auditing')


class CoreConfig(AppConfig):
    name = 'IPTVAdmin.core'
    verbose_name = 'IPTV Admin'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
