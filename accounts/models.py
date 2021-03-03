import bcrypt

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=63) # 63 ou 60? testei no terminal e a hash criada sempre deu 60, ao passar o model vai para 63. django altera o salt?

    def save(self, *args, **kwargs):
        self.full_clean()
        self.password = self.encrypt_password(self.password)
        super().save(*args, **kwargs)

    def encrypt_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed


class Session(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=64)
