import json
from rstr import rstr, letters, nonwhitespace
import jwt

from django.test import TestCase, Client
from django.db import models
from django.urls import reverse


from ..models import User


class SignUp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_creates_user(self):
        payload = {
                    "username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com",
                    "password": f"{rstr(nonwhitespace(), 7)}"
                    }
        result = self.client.post(reverse("create_user"), payload, content_type="application/json")
        user = User.objects.filter(username=payload["username"])
        self.assertTrue(user.exists())
        self.assertEqual(user.first().username, payload["username"])
        self.assertEqual(result.status_code, 201)

    def test_sign_up_encrypts_password(self):
        payload = {
                    "username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com",
                    "password": f"{rstr(letters(), 10, 20)}-"
                    }
        self.client.post(reverse("create_user"), payload, content_type="application/json")
        stored_password = User.objects.get(username=payload["username"]).password
        self.assertEqual(len(stored_password), 60)

    def test_sign_up_responds_error_if_password_is_not_provided(self):
        payload = {
                    "username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com"
                    }
        expected_result = {'password': ['This field is required.']}
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_not_provided(self):
        payload = {
                    "password": f"{rstr(nonwhitespace(), 10, 20)}"
                    }
        expected_result = {'username': ['This field is required.']}
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_empty_string(self):
        payload = {
                    "username": "",
                    "password": f"{rstr(nonwhitespace(), 7)}"
                    }
        expected_result = {'username': ['This field is required.']}
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_password_is_too_short(self):
        payload = {
                    "username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com",
                    "password": f"{rstr(nonwhitespace(), 6)}"
                    }
        expected_result = {'password': ['Ensure this value has at least 7 characters (it has 6).']}
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_too_short(self):
        payload = {
                    "username": f"{rstr(letters(), 4)}",
                    "password": f"{rstr(nonwhitespace(), 7)}"
                    }
        expected_result = '{"username": ["Enter a valid email address.", "Ensure this value has at least 5 characters (it has 4)."]}'
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        self.maxDiff = None
        self.assertEqual(result.content.decode(), expected_result)

    def test_sign_up_responds_error_if_username_is_already_picked(self):
        payload = {
                    "username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com",
                    "password": f"{rstr(nonwhitespace(), 7)}"
                    }
        self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.client.post(reverse('create_user'), payload, content_type="application/json")
        expected_result = {'username': ['User with this Username already exists.'],}
        result = self.client.post(reverse('create_user'), payload, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.json(), expected_result)

    def test_create_user_endpoint_responds_access_token(self):
        payload = {"username": f"{rstr(letters(), 5, 50)}@{rstr(letters(), 4, 40)}.com",
                   "password": f"{rstr(nonwhitespace(), 7)}"}
        result = self.client.post(reverse("create_user"), payload, content_type="application/json")
        token = jwt.decode(result["access_token"],
                           options={"verify_signature": False})
        self.assertEqual(token["usr"], payload["username"])
