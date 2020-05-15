from django.db.models import Sum, Q

from ticket_admin.core.manager import Manager
from ticket_admin.custom_profile import models


class ProfileUserManager(Manager):

    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def get_billing(self, user):
        result = self.filter(
            Q(status=models.ProfileUser.ACTIVE) |
            Q(status=models.ProfileUser.WAITING),
            profile__user=user
        ).aggregate(total=Sum('value')).get('total')
        if result:
            return result
        return 0

    def get_billing_liquid(self, user):
        user_total = self.filter(
            Q(status=models.ProfileUser.ACTIVE) |
            Q(status=models.ProfileUser.WAITING),
            profile__user=user
        ).aggregate(total=Sum('value')).get('total')
        panel_total = self.filter(profile__user=user).aggregate(total=Sum('panel__value')).get('total')
        if user_total and panel_total:
            return user_total - panel_total
        return 0
