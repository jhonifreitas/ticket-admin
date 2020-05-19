from django.db.models import Sum

from ticket_admin.core.manager import Manager
from ticket_admin.custom_profile import models


class ProfileUserManager(Manager):

    def get_billing(self, user):
        result = self.filter(
            profile__user=user).exclude(status=models.ProfileUser.EXPIRED).aggregate(total=Sum('value')).get('total')
        if result:
            return result
        return 0

    def get_billing_liquid(self, user):
        user_total = self.filter(
            profile__user=user).exclude(status=models.ProfileUser.EXPIRED).aggregate(total=Sum('value')).get('total')
        panel_total = self.filter(
            profile__user=user).exclude(
                status=models.ProfileUser.EXPIRED).aggregate(total=Sum('panel__value')).get('total')
        if user_total and panel_total:
            return user_total - panel_total
        return 0
