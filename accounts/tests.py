import json
import bcrypt

from django.test import TestCase, Client
from django.db import models
from django.http import JsonResponse
from django.urls import reverse

from .models import User
from .views import check_endpoint_status, SignUp, SignIn


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
        self.create_user_post_request_data = {"username": "johnsmith", "email": "john@gmail.com", "password": "abc123-"}
        

    def test_sign_up_creates_user(self):
        result = self.client.post(reverse('create_user'), self.create_user_post_request_data, content_type="application/json")
        expected_result = JsonResponse({"user_created": "ok"})
        user = User.objects.filter(email="john@gmail.com")
        self.assertTrue(user.exists())
        self.assertEqual("johnsmith", User.objects.get(email="john@gmail.com").username)
        self.assertEqual(expected_result.content, result.content)
        self.assertEqual(result.status_code, 201)


    def test_sign_up_encrypts_password(self):
        # dúvida: ValueError: Invalid salt quando uso a checkpw() e a hash produzida pelo endpoint, não essa criada de dentro do teste
        self.client.post(reverse('create_user'), self.create_user_post_request_data, content_type="application/json")
        stored_password = User.objects.get(email="john@gmail.com").password
        self.assertEqual(len(stored_password), 63)

class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = bcrypt.hashpw("abc123-".encode(), bcrypt.gensalt())
        self.user = User.objects.create(username="cardoso", email="cardoso@anon.com", password=self.password)

    def test_sign_in_validates_hashed_password(self):
        create_session_post_request_data = {"username": "cardoso", "password": "abc123-"}
        self.client.post("create_session", create_session_post_request_data, content_type="application/json")
        session = Session.objects.get(user_id=self.user.id)
        self.assertTrue(session)
        self.assertTrue(bcrypt.checkpw(password.encode(), hashed))        

    def test_sign_in_creates_session_token(self):
        create_session_post_request_data = {"username": "cardoso", "password": "abc123-"}
        result = self.client.post("create_session", create_session_post_request_data, content_type="application/json")
        self.assertTrue(result.COOKIES)