import json
from datetime import datetime
from django.db.models import Sum

from ticket_admin.core.manager import Manager
from ticket_admin.custom_profile import models


class ProfileUserManager(Manager):

    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def get_billing(self, user):
        object_list = self.filter(
            status=models.ProfileUser.ACTIVE,
            profile__user=user,
            expiration__year=datetime.now().year
        ).values('expiration__month').annotate(total=Sum('value')).order_by()
        result = []
        for month in self.MONTHS:
            total = 0
            obj = [obj for obj in object_list if obj.get('expiration__month') == month]
            if any(obj):
                total = "{:.2f}".format(obj[0].get('total'))
            result.append(total)
        return json.dumps(result)
