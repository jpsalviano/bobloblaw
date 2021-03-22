import jwt
import json

from django.test import TestCase, Client
from django.urls import reverse
from django.core.signing import Signer

from ..models import User


class AuthJWT(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")

    def test_auth_jwt_generates_token(self):
        payload = {"user_id": self.user.id}
        result = self.client.post(reverse("auth_jwt"), payload, content_type="application/json")
        secret_key = Signer().sign("JWT")
        expected_result = json.dumps({"token": jwt.encode(payload, secret_key, "HS256")})
        self.assertEqual(result.content.decode(), expected_result)

    def test_auth_jwt_token_holds_correct_payload(self):
        payload = {"user_id": self.user.id}
        result = self.client.post(reverse("auth_jwt"), payload, content_type="application/json")
        secret_key = Signer().sign("JWT")
        result_token = result.json()["token"]
        payload_from_result_token = jwt.decode(result_token, secret_key, algorithms=["HS256"])
        self.assertEqual(payload_from_result_token, payload)
