import jwt
import datetime

from django.core.signing import Signer

from ..models import User


def _generate_token(username):
    user_id = User.objects.filter(username=username).first().id
    secret_key = Signer().sign("JWT")
    payload = {
        "usr": username,
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=84600)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
