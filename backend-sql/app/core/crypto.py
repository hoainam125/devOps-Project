from datetime import datetime, timedelta, timezone
from app.core.config import settings
import os
import base64
import hashlib
import json
import hmac
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = settings()
def urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def urlsafe_b64decode(data: str) -> bytes:
    padded = data + '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded)

def create_access_token(data: dict, expires_delta: timedelta = None):
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
        settings.SECRET_KEY.encode(), 
        f"{header_encoded}.{payload_encoded}".encode(), 
        hashlib.sha256
    ).digest()
    
    signature_encoded = urlsafe_b64encode(signature)
    
    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

def verify_token(token: str, credentials_exception):
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        payload = json.loads(urlsafe_b64decode(payload_b64))
        
        expire = datetime.fromisoformat(payload["exp"])
        if expire < datetime.now(timezone.utc):
            raise credentials_exception
        
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(), 
            f"{header_b64}.{payload_b64}".encode(), 
            hashlib.sha256
        ).digest()
        
        if not hmac.compare_digest(signature_b64, urlsafe_b64encode(expected_signature)):
            raise credentials_exception
        
        return payload
    except (ValueError, KeyError, json.JSONDecodeError):
        raise credentials_exception

# Exception for invalid credentials
class CredentialsException(Exception):
    pass