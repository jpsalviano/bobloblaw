import json

from django.test import TestCase, Client
from django.db import models
from django.urls import reverse


from ..models import User


class SignUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload = {"username": "johnsmith",
                        "email": "john@gmail.com",
                        "password": "abc123-"}

    def test_sign_up_creates_user(self):
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        user = User.objects.filter(email="john@gmail.com")
        expected_result = {"username": "johnsmith", "email": "john@gmail.com"}
        self.assertTrue(user.exists())
        self.assertEqual(user.first().username, expected_result["username"])
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.content.decode(), json.dumps(expected_result))

    def test_sign_up_encrypts_password(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        stored_password = User.objects.get(email="john@gmail.com").password
        self.assertEqual(len(stored_password), 60)

    def test_sign_up_responds_error_if_password_is_not_provided(self):
        del self.payload["password"]
        expected_result = {'password': ['This field is required.']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_not_provided(self):
        del self.payload["username"]
        expected_result = {'username': ['This field is required.']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_email_is_not_provided(self):
        self.payload["email"] = ""
        expected_result = {'email': ['This field is required.']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_password_is_too_short(self):
        self.payload["password"] = "abc12-"
        expected_result = {'password': ['Ensure this value has at least 7 characters (it has 6).']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_too_short(self):
        self.payload["username"] = "jao"
        expected_result = {'username': ['Ensure this value has at least 5 characters (it has 3).']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_too_long(self):
        self.payload["username"] = "jao"*7
        expected_result = {'username': ['Ensure this value has at most 20 characters (it has 21).']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)

    def test_sign_up_responds_error_if_username_is_already_picked(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        expected_result = {'email': ['User with this Email already exists.'],
                           'username': ['User with this Username already exists.']}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 400)
