import bcrypt

from django.db import models

class User(models.Model):
    # id = models.AutoField(primary_key=True) is set by default by Django
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=72)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = False

    def save(self, *args, **kwargs):
        self.full_clean()
        self.password = self.encrypt_password(self.password)
        super().save(*args, **kwargs)

    def encrypt_password(self, password_txt):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_txt.encode(), salt)
        return password_hash.decode()
