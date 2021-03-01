from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username=username, email=email, password=password)
        return user
