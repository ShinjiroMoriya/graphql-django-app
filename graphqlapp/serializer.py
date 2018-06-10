from datetime import timedelta
from django.conf import settings
from itsdangerous import (
    URLSafeSerializer, BadSignature,
    TimedJSONWebSignatureSerializer
)


serializer_key = URLSafeSerializer(settings.SECRET_KEY)


def time_seconds(days=7):
    return timedelta(days=days).total_seconds()


def token_timed(expires=None):
    if expires is None:
        expires = time_seconds(7)

    return TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,
        expires_in=expires)


def serializer_dumps(value: str or dict) -> str or None:
    """
    シリアライズ化
    """
    try:
        return serializer_key.dumps(value)
    except BadSignature:
        return None


def serializer_time_dumps(value: str or dict, expires=None) -> str or None:
    """
    シリアライズ化 有効期限あり
    """
    serializer_time_key = token_timed(expires)

    try:
        return serializer_time_key.dumps(value).decode("utf-8")

    except BadSignature:
        return None


def serializer_loads(value: str) -> dict or str or None:
    try:
        if value is not None:
            return serializer_key.loads(value)
        else:
            return None
    except BadSignature:
        return None


def serializer_time_loads(value: str, expires=None) -> dict or str or None:
    serializer_time_key = token_timed(expires)
    try:
        if value is not None:
            return serializer_time_key.loads(value)

        else:
            return None

    except BadSignature:
        return None
