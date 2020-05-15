from django.db.models import Sum, Q

from ticket_admin.core.manager import Manager
from ticket_admin.custom_profile import models


class ProfileUserManager(Manager):

    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def get_billing(self, user):
        queryset = self.filter(
            Q(status=models.ProfileUser.ACTIVE) |
            Q(status=models.ProfileUser.WAITING),
            profile__user=user
        ).values('value').annotate(total=Sum('value')).order_by()
        if queryset:
            return queryset[0].get('total')
        return 0

    def get_billing_liquid(self, user):
        query_user = self.filter(
            Q(status=models.ProfileUser.ACTIVE) |
            Q(status=models.ProfileUser.WAITING),
            profile__user=user
        ).values('value').annotate(total=Sum('value')).order_by()
        query_panel = self.filter(
            profile__user=user).values('panel').annotate(total=Sum('panel__value')).order_by()
        if query_user and query_user:
            return query_user[0].get('total') - query_panel[0].get('total')
        return 0
