import jwt
import time

from django.core.signing import Signer

from ..models import User


def _generate_token(username):
    user_id = User.objects.filter(username=username).first().id
    secret_key = Signer().sign("JWT")
    payload = {
        "sub": user_id,
        "exp": time.time() + 86400,
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
