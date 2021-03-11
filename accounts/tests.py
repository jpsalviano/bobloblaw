import json
import bcrypt

from django.test import TestCase, Client
from django.db import models
from django.http import JsonResponse
from django.urls import reverse
from django.core import exceptions

from .models import User, Session
from .views import check_endpoint_status
from .sign_up import SignUp
from .sign_in import SignIn


class UserModelTestCase(TestCase):

    def test_user_model_class(self):
        user = User.objects.create(username="cardoso",
                                   email="cardoso@anon.com",
                                   password="abc123-")
        self.assertTrue(hasattr(user, "username"))
        self.assertTrue(hasattr(user, "email"))
        self.assertTrue(hasattr(user, "password"))


class EndpointStatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_check_endpoint_status(self):
        expected_result = JsonResponse({"status": "ok"})
        result = self.client.get(reverse('check_status'))
        self.assertEqual(result.content, expected_result.content)
        self.assertEqual(result.status_code, 200)


class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload = {"username": "johnsmith",
                        "email": "john@gmail.com",
                        "password": "abc123-",}

    def test_sign_up_creates_user(self):
        expected_result = {"username": "johnsmith", "email": "john@gmail.com"}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        user = User.objects.filter(email="john@gmail.com")
        self.assertTrue(user.exists())
        self.assertEqual(user.first().username, expected_result["username"])
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 201)

    def test_sign_up_encrypts_password(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        stored_password = User.objects.get(email="john@gmail.com").password
        self.assertEqual(len(stored_password), 60)

    def test_sign_up_responds_error_if_passwords_are_too_short(self):
        self.payload["password"] = "abc12-"
        expected_result = {"error": "Password must be at least 7 characters long."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        user = User.objects.filter(email="john@gmail.com")
        self.assertFalse(user.exists())

    def test_sign_up_responds_error_if_password_is_not_provided(self):
        del self.payload["password"]
        expected_result = {"error": "You must enter a password."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        user = User.objects.filter(email="john@gmail.com")
        self.assertFalse(user.exists())

    def test_sign_up_responds_error_if_username_was_not_entered(self):
        self.payload["username"] = ""
        expected_result = {"error": "Username cannot be null."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)

    def test_sign_up_responds_error_if_username_is_too_short_or_too_long(self):
        self.payload["username"] = "jao"
        expected_result = {"error": "Username is too short."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        
        self.payload["username"] = "jao"*7
        expected_result = {"error": "Username is too long."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        
        user = User.objects.filter(email="john@gmail.com")
        self.assertFalse(user.exists())

    def test_sign_up_responds_error_if_username_is_already_picked(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        expected_result = {"error": "Username is already picked."}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)

    def test_sign_up_responds_error_if_email_is_already_in_use(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        expected_result = {"error": "Email is already in use."}
        self.payload["username"] = "smithjohn"
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso",
                                        email="cardoso@anon.com",
                                        password="abc123-")

    def test_sign_in_validates_hashed_password(self):
        payload = {"username": "cardoso", "password": "abc123-"}
        expected_result = {"username": "cardoso"}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(len(result.json()["session_token"]), 64)
        self.assertEqual(result.status_code, 201)

    def test_sign_in_creates_and_responds_session_token(self):
        payload = {"username": "cardoso", "password": "abc123-"}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(len(result.json()["session_token"]), 64)
        self.assertEqual(result.status_code, 201)
        session = Session.objects.get(user=self.user.id)
        self.assertTrue(hasattr(session, "session_token"))
        self.assertEqual(len(session.session_token), 64)
        self.assertEqual(session.session_token, result.json()["session_token"])

    def test_sign_in_does_not_validate_wrong_password(self):
        payload = {"username": "cardoso", "password": "-abc123"}
        expected_result = {"error": "Wrong password."}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
        session = Session.objects.filter(user=self.user.id)
        self.assertFalse(session.exists())

    def test_sign_in_responds_error_non_existent_username_is_entered(self):
        payload = {"username": "cardoso123", "password": "-abc123"}
        expected_result = {"error": "Username does not exist."}
        result = self.client.post(reverse("create_session"), payload, content_type="application/json")
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 403)
