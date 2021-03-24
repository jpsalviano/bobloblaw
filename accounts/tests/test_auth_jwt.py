import jwt
import json
import time

from django.test import TestCase, Client
from django.urls import reverse
from django.core.signing import Signer

from ..models import User


class AuthJWT(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso@anon.com",
                                        password="abc123-")
'''
    def test_auth_jwt_generates_token(self):
        payload = {"username": self.user.username}
        result = self.client.post(reverse("auth_jwt"), payload, content_type="application/json")
        secret_key = Signer().sign("JWT")
        self.assertTrue(result.content)

    def test_auth_jwt_token_holds_correct_payload(self):
        payload = {"username": self.user.username}
        result = self.client.post(reverse("auth_jwt"), payload, content_type="application/json")
        secret_key = Signer().sign("JWT")
        result_token = result.content
        payload_from_result_token = jwt.decode(result_token, secret_key, algorithms=["HS256"])
        self.assertTrue(payload_from_result_token)'''