from django.db import models


class User(models.Model):
    self.username = models.CharField(max_length=30, unique=True)
    self.email = models.EmailField()
    self.password = models.CharField(max_length=100)

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username=username, email=email, password=password)
        return user

    @classmethod
    def get_user(cls):
        self.username
