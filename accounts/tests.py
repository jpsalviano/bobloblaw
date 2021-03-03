import json

from django.test import TestCase, Client
from django.db import models
from django.http import JsonResponse

from .models import User
from .views import check_endpoint_status, SignUp


class UserModelTestCase(TestCase):

    def test_user_model_class(self):
        user = User.objects.create(username="cardoso", email="cardoso@anon.com", password="abc123-")
        self.assertTrue(hasattr(user, "username"))
        self.assertTrue(hasattr(user, "email"))
        self.assertTrue(hasattr(user, "password"))


class EndpointStatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_check_endpoint_status(self):
        expected_result = JsonResponse({"status": "ok"})
        result = self.client.get("/accounts/status/")
        self.assertEqual(result.content, expected_result.content)
        self.assertEqual(result.status_code, 200)


class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_endpoint_creates_user(self):
        post_request_data = {"username": "johnsmith", "email": "john@gmail.com", "password": "abc123-"}
        expected_result = JsonResponse({"user_created": "ok"})
        result = self.client.post("/accounts/signup/", post_request_data, content_type="application/json")
        user = User.objects.filter(email="john@gmail.com")
        self.assertTrue(user.exists())
        self.assertEqual(expected_result.content, result.content)


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()