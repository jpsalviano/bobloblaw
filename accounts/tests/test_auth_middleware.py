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

    def test_auth_middleware_responds_401_if_no_token_set(self):
        get_private_request = self.client.get(
                                              reverse("private"),
                                              {},
                                              content_type="application/json"
                                            )
        self.assertEqual(get_private_request.status_code, 401)

    def test_auth_middleware_responds_401_if_invalid_token_set(self):
        get_private_request = self.client.get(
                                              reverse("private"),
                                              {'access_token': 'invalid'},
                                              content_type="application/json"
                                            )
        self.assertEqual(get_private_request.status_code, 401)

    def test_auth_middleware_responds_200_if_valid_token_set(self):
        valid_signin_response = self.client.post(reverse("sign_in"), self.payload, content_type="application/json")
        valid_access_token = valid_signin_response._headers.get("access_token")[1]
        valid_access_token_payload = jwt.decode(valid_access_token, self.sign, algorithms=["HS256"])
        post_private_request = self.client.post(reverse("private"),
                                              {"access_token" : valid_access_token},
                                              content_type="application/json"
                                            )
        self.assertEqual(post_private_request.status_code, 200)
