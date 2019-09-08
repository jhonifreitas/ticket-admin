import json
from datetime import datetime
from django.db.models import Sum

from IPTVAdmin.core.manager import Manager


class BilletManager(Manager):

    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def get_billing(self):
        object_list = self.filter(
            dueDate__year=datetime.now().year
        ).values('dueDate__month').annotate(total=Sum('amount')).order_by()
        result = []
        for month in self.MONTHS:
            total = 0
            obj = [obj for obj in object_list if obj.get('dueDate__month') == month]
            if any(obj):
                total = "{:.2f}".format(obj[0].get('total'))
            result.append(total)
        return json.dumps(result)
