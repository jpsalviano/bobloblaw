from rstr import rstr, letters, nonwhitespace
import jwt
import json

from django.test import Client, TestCase
from django.urls import reverse
from django.core.signing import Signer

from ..models import User
from ..auth_tools.auth_jwt import _generate_token


class AuthMiddleware(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com"
        self.password = f"{rstr(nonwhitespace(), 7, 60)}"
        self.payload = {"username": self.username, "password": self.password}
        self.user = User.objects.create(username=self.username, password=self.password)
        self.sign = Signer().sign("JWT")

    def test_auth_middleware_responds_401_if_invalid_token_set(self):
        get_private_request = self.client.get(reverse("private"), {'access_token': 'invalid'})
        self.assertEqual(get_private_request.status_code, 401)

    def test_auth_middleware_responds_200_if_valid_token_set(self):
        valid_access_token = _generate_token(self.username)
        get_private_request = self.client.get(reverse("private"), {'access_token': valid_access_token})
        self.assertEqual(get_private_request.status_code, 401)
