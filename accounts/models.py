from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)


class Session(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=256)
