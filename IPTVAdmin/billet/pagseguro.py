import json
import requests
from xmljson import parker
from xml.etree.ElementTree import fromstring

from django.conf import settings

from IPTVAdmin.custom_profile.models import Profile


class Pagseguro:

    def __init__(self, config):
        self.config = config

    def xml_to_json(self, response):
        return parker.data(fromstring(response.text))

    def get_credencials(self):
        return f'?email={self.config.user.email}&token={self.config.token}'

    def get_transactions(self, initial_date, final_date):
        url = f'{settings.PAGSEGURO_TRANSACOES_URL}{self.get_credencials()}'
        url += f'&initialDate={initial_date}T00:00'
        url += f'&finalDate={final_date}T00:00'

        response = requests.get(url)
        result_json = self.xml_to_json(response)

        if response.ok:
            if result_json.get('resultsInThisPage'):
                transactions = []
                if isinstance(result_json.get('transactions'), list):
                    for transaction in result_json.get('transactions'):        
                        transactions.append(self.appendTransaction(transaction))
                else:
                    transactions.append(self.appendTransaction(result_json.get('transactions').get('transaction')))
                result = {'ok': self.appendTransaction(transactions)}
            else:
                result = {'warning': 'Nenhum boleto importado!'}
        else:
            result = {'error': result_json.get('error').get('message')}
        return result
    
    def appendTransaction(self, transaction):
        if transaction.get('type') == 1 and transaction.get('paymentMethod').get('type') == 2:
            obj = self.get_transaction(transaction.get('code'))
            if obj:
                return obj

    def get_transaction(self, code):
        url = f'{settings.PAGSEGURO_TRANSACOES_URL}/{code}{self.get_credencials()}'

        response = requests.get(url)
        result_json = self.xml_to_json(response)

        if response.ok:
            obj = {
                'profile': Profile.objects.get(email=result_json.get('sender').get('email')),
                'code': result_json.get('code'),
                'paymentLink': result_json.get('paymentLink'),
                'reference': result_json.get('reference'),
                'instructions': self.config.instructions_billet,
                'description': result_json.get('items').get('item').get('description'),
                'status': result_json.get('status'),
                'amount': result_json.get('netAmount'),
            }
            result = obj
        else:
            result = None
        return result

    def generate_ticket(self, data):
        url = f'{settings.PAGSEGURO_BOLETO_URL}{self.get_credencials()}'

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
            }
        }
        return requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
