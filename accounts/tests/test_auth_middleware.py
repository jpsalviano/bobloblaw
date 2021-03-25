from rstr import rstr, letters, nonwhitespace
import jwt
import json

from django.test import Client, TestCase
from django.urls import reverse
from django.core.signing import Signer

from ..auth_tools.auth_middleware import auth_middleware
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
        sign_right_credentials_in = self.client.post(reverse("sign_in"), self.payload, content_type="application/json")
        encoded_access_token = json.loads(sign_right_credentials_in.content.decode())["access_token"]
        access_token_dict = jwt.decode(encoded_access_token, self.sign, algorithms=["HS256"])
        self.assertEqual(access_token_dict["sub"], self.user.id)
        self.assertEqual(access_token_dict["usr"], self.user.username)
        self.payload["access_token"] = access_token_dict
        sign_in_get_request = self.client.post(reverse("sign_in"), self.payload, content_type="application/json")
        sign_in_get_request_json_resp = json.loads(sign_in_get_request.content.decode())
        self.assertEqual(sign_in_get_request_json_resp["logged"], True)
