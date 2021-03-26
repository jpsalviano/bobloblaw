import jwt
import json
import time
from rstr import rstr, letters, nonwhitespace

from django.test import TestCase, Client
from django.urls import reverse
from django.core.signing import Signer

from ..models import User
from ..auth_tools.auth_jwt import _generate_token


class AuthJWT(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username=f"{rstr(letters(), 5)}@{rstr(letters(), 4)}.com",
                                        password=f"{rstr(nonwhitespace(), 7)}")

    def test_auth_jwt_generates_token(self):
        token = _generate_token(self.user.username)
        decoded_payload = jwt.decode(token, options={"verify_signature": False})
        self.assertTrue(token)

    def test_auth_jwt_token_holds_correct_payload(self):
        secret_key = Signer().sign("JWT")
        token = _generate_token(self.user.username)
        payload_from_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        self.assertTrue(payload_from_token)
        self.assertEqual(payload_from_token["usr"], self.user.username)
        self.assertEqual(payload_from_token["sub"], self.user.id)
        self.assertTrue(isinstance(payload_from_token["exp"], float))
