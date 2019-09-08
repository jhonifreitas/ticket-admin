from model_mommy import mommy

from django.urls import reverse_lazy
from django.test import TestCase


class BaseTestCase(TestCase):

    def setUp(self):
        self.username = 'test'
        self.password = 'test'
        self.create_user()
        self.create_config()
        self.login()

    def create_user(self):
        self.user = mommy.make('auth.User', username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def create_config(self):
        self.config = mommy.make('core.Config', user=self.user)

    def login(self):
        self.client.post(reverse_lazy('profile:login'), {'username': self.user.username, 'password': self.password})
