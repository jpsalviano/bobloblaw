from rstr import rstr, letters, nonwhitespace
import jwt
import json

from django.test import Client, TestCase
from django.urls import reverse
from django.core.signing import Signer

from ..models import User


class AuthMiddleware(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com"
        self.password = f"{rstr(nonwhitespace(), 7, 60)}"
        self.payload = {"username": self.username, "password": self.password}
        self.user = User.objects.create(username=self.username, password=self.password)
        self.sign = Signer().sign("JWT")

    def test_auth_middleware_reads_access_token(self):
        pass