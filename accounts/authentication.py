import base64
import binascii
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


def _base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_access_token(user):
    now = int(time.time())
    expiry_seconds = getattr(settings, "JWT_ACCESS_TOKEN_LIFETIME_SECONDS", 86400)

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user.id,
        "email": user.email,
        "password_hash": user.get_session_auth_hash(),
        "iat": now,
        "exp": now + expiry_seconds,
    }

    encoded_header = _base64url_encode(
        json.dumps(header, separators=(",", ":")).encode("utf-8")
    )
    encoded_payload = _base64url_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    return f"{encoded_header}.{encoded_payload}.{_base64url_encode(signature)}"


def decode_access_token(token):
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise exceptions.AuthenticationFailed("Invalid token") from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    expected_signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    try:
        received_signature = _base64url_decode(encoded_signature)
    except (ValueError, binascii.Error) as exc:
        raise exceptions.AuthenticationFailed("Invalid token") from exc

    if not hmac.compare_digest(received_signature, expected_signature):
        raise exceptions.AuthenticationFailed("Invalid token")

    try:
        payload = json.loads(_base64url_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError) as exc:
        raise exceptions.AuthenticationFailed("Invalid token") from exc

    if payload.get("exp", 0) < int(time.time()):
        raise exceptions.AuthenticationFailed("Token has expired")

    return payload


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth:
            return None

        if auth[0].lower() != self.keyword.lower().encode("ascii"):
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        token = auth[1].decode("ascii")
        payload = decode_access_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token")

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("User not found") from exc

        if payload.get("password_hash") != user.get_session_auth_hash():
            raise exceptions.AuthenticationFailed("Token has expired")

        return user, token
