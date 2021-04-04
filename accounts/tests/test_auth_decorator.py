import json
from rstr import rstr, letters, nonwhitespace

from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from ..auth_tools.auth_decorator import login_required
from ..models import User
from ..views.private import Private


class AuthDecorator(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com"
        self.password = f"{rstr(nonwhitespace(), 7, 60)}"
        self.user = User.objects.create(username=self.username, password=self.password)
        self.payload = {"username": self.username, "password": self.password}

    def test_get_private_endpoint_responds_403_status_code(self):
        get_request_private = self.client.get(reverse("private"), self.payload,
                                               content_type="application/json")
        self.assertEqual(get_request_private.status_code, 403)
        self.assertEqual(get_request_private.content.decode(),
                         json.dumps({"error": ["Forbidden."]}))

    def test_get_private_endpoint_responds_200_status_code_if_valid_token_set(self):
        valid_signin_response = self.client.post(reverse("sign_in"), self.payload,
                                                 content_type="application/json")
        valid_access_token = valid_signin_response._headers.get("access_token")[1]
        post_request_private = self.client.post(reverse("private"),
                                                {"access_token": valid_access_token},
                                                content_type="application/json")
        self.assertEqual(post_request_private.status_code, 200)
        self.assertEqual(post_request_private.content.decode(),
                         json.dumps({"username": 1}))

    