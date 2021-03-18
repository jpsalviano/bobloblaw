import bcrypt

from django.db import models

class User(models.Model):
    # id = models.AutoField(primary_key=True) is set by default by Django
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.password = self.encrypt_password(self.password)
        super().save(*args, **kwargs)

    def encrypt_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
