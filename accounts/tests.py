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
        user = User.objects.create(username="cardoso", email="cardoso@anon.com", password="abc123-")
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
                        "password1": "abc123-",
                        "password2": "abc123-"}

    def test_sign_up_creates_user(self):
        expected_result = {"user_created": "ok"}
        result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        user = User.objects.filter(email="john@gmail.com")
        self.assertTrue(user.exists())
        self.assertEqual("johnsmith", user.first().username)
        self.assertEqual(result.json(), expected_result)
        self.assertEqual(result.status_code, 201)

    def test_sign_up_encrypts_password(self):
        self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        stored_password = User.objects.get(email="john@gmail.com").password
        self.assertEqual(len(stored_password), 60)

    def test_sign_up_raises_validation_error_exception_if_passwords_are_different(self):
        self.payload["password2"] = "-abc123"
        with self.assertRaises(exceptions.ValidationError) as error:
            result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(error.exception.message, "Passwords do not match.")
        user = User.objects.filter(email="john@gmail.com")
        self.assertFalse(user.exists())

    def test_sign_up_raises_validation_error_ir_username_is_too_short(self):
        self.payload["username"] = "jao"
        with self.assertRaises(exceptions.ValidationError) as error:
            result = self.client.post(reverse('create_user'), self.payload, content_type="application/json")
        self.assertEqual(error.exception.message, "Username is too short.")
        user = User.objects.filter(email="john@gmail.com")
        self.assertFalse(user.exists())


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="cardoso", email="cardoso@anon.com", password="abc123-")

    def test_sign_in_validates_hashed_password(self):
        create_session_post_request_data = {"username": "cardoso", "password": "abc123-"}
        self.client.post(reverse("create_session"), create_session_post_request_data, content_type="application/json")
        session = Session.objects.filter(user=self.user.id)
        self.assertTrue(session.exists())

    def test_sign_in_does_not_validate_wrong_password(self):
        create_session_post_request_data = {"username": "cardoso", "password": "-abc123"}
        result = self.client.post(reverse("create_session"), create_session_post_request_data, content_type="application/json")
        self.assertEqual(result.json(), {"error": "wrong password"})
        session = Session.objects.filter(user=self.user.id)
        self.assertFalse(session.exists())

    def test_sign_in_creates_session_token(self):
        create_session_post_request_data = {"username": "cardoso", "password": "abc123-"}
        result = self.client.post(reverse("create_session"), create_session_post_request_data, content_type="application/json")
        self.assertEqual(result.json(), {"logged": "true"})
        session = Session.objects.get(user=self.user.id)
        self.assertTrue(hasattr(session, "session_token"))
        self.assertEqual(len(session.session_token), 64)
