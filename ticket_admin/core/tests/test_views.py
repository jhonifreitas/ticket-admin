from django.urls import reverse_lazy

from ticket_admin.core.tests.helpers import BaseTestCase


class HomeTest(BaseTestCase):

    def setUp(self):
        super(HomeTest, self).setUp()
        self.response = self.client.get(reverse_lazy('core:home'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')
