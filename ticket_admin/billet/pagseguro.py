import json
import requests
from xmljson import parker
from xml.etree.ElementTree import fromstring

from django.urls import reverse_lazy


class Pagseguro:

    url = 'https://ws.pagseguro.uol.com.br'
    host = 'https://ticket-painel.herokuapp.com'
    notification_url = reverse_lazy('api.v1:notification')

    def xml_to_json(self, response):
        return parker.data(fromstring(response.text))

    def set_config(self, config):
        self.config = config

    def get_credencials(self):
        return f'?email={self.config.user.email}&token={self.config.token}'

    def get_notification(self, code):
        url = '{}/v2/transactions/notifications/{}'.format(self.url, code)
        return requests.get(url)

    def get_transaction(self, code):
        url = '{}/v2/transactions/{}{}'.format(self.url, code, self.get_credencials())

        result = None
        response = requests.get(url)
        result_json = self.xml_to_json(response)

        if response.ok:
            result = {
                'code': result_json.get('code'),
                'paymentLink': result_json.get('paymentLink'),
                'reference': result_json.get('reference'),
                'description': result_json.get('items').get('item').get('description'),
                'status': result_json.get('status'),
                'amount': result_json.get('netAmount'),
            }
        return result

    def generate_ticket(self, data):
        url_billet = '/recurring-payment/boletos'
        url = '{}{}{}'.format(self.url, url_billet, self.get_credencials())

        data = {
            "reference": data.get('profile').name,
            "firstDueDate": str(data.get('dueDate')),
            "numberOfPayments": data.get('numberOfPayments'),
            "periodicity": "monthly",
            "amount": data.get('amount'),
            "instructions": data.get('instructions'),
            "description": data.get('description'),
            "customer": {
                "document": {
                    "type": "CPF",
                    "value": data.get('profile').cpf
                },
                "name": data.get('profile').name,
                "email": data.get('profile').email,
                "phone": {
                    "areaCode": data.get('profile').phone[:2],
                    "number": data.get('profile').phone[2:]
                }
            },
            'notificationURL': '{}{}'.format(self.host, self.notification_url)
        }
        return requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
