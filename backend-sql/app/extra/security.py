from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, FastAPI
import base64
import hashlib
import json
import hmac
from passlib.context import CryptContext
from redis import Redis
from . import config
from .RedisStorage import RedisStorage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = config.get_config()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def urlsafe_b64decode(data: str) -> bytes:
    padded = data + '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded)

def create_access_token(data: dict, store: RedisStorage, expires_delta: timedelta = None):
    uid = data.get("uid", None)
    assert uid is not None
    secret = str(uid) + settings.SECRET_KEY + datetime.now().isoformat()
    store.set(uid, secret, ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.isoformat()})

    header_encoded = urlsafe_b64encode(json.dumps(header).encode())
    payload_encoded = urlsafe_b64encode(json.dumps(to_encode).encode())
    signature = hmac.new(
        secret.encode(),
        f"{header_encoded}.{payload_encoded}".encode(),
        hashlib.sha256
    ).digest()

    signature_encoded = urlsafe_b64encode(signature)

    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

def verify_token(token: str, store: RedisStorage):
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        payload = json.loads(urlsafe_b64decode(payload_b64))

        expire = datetime.fromisoformat(payload["exp"])
        if expire < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        uid = payload.get("uid", None)
        assert uid is not None
        secret = store.get(uid)
        if not secret:
            raise HTTPException(status_code=401, detail="Token invalid")
        if isinstance(secret, bytes):
            secret = secret.decode()

        expected_signature = hmac.new(
            secret.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(signature_b64, urlsafe_b64encode(expected_signature)):
            raise HTTPException(status_code=401, detail="Token signature does not match")

        return payload
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Token could not be decoded")