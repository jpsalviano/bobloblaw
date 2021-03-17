import bcrypt

from django.db import models
from django.forms import ModelForm


class User(models.Model):
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


class SignUpForm(ModelForm):
    
    class FormFields(models.Model):
        username = models.CharField(max_length=30, unique=True)
        email = models.EmailField(unique=True)
        password = models.CharField(max_length=60)
        password2 = models.CharField(max_length=60)

    class Meta:
        model = super(FormFields)
        fields = ["username", "email", "password", "password2"]