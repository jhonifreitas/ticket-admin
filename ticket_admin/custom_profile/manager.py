from django.db.models import Sum

from ticket_admin.core.manager import Manager
from ticket_admin.custom_profile import models


class ProfileUserManager(Manager):

    def get_billing(self, user):
        result = self.filter(
            profile__user=user).exclude(status=models.ProfileUser.EXPIRED).aggregate(total=Sum('value')).get('total')
        if result:
            return round(result, 2)
        return 0

    def get_credit_costs(self, user):
        result = self.filter(
            profile__user=user).exclude(
                status=models.ProfileUser.EXPIRED).aggregate(total=Sum('panel__value')).get('total')
        if result:
            return round(result, 2)
        return 0
