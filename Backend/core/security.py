from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings

password_hasher = PasswordHasher()

def hash_password(password:str)-> str:
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password:str)-> bool:
    try:
        password_hasher.verify(
            hashed_password,
            plain_password
        )
        return True
    except Exception:
        return False

def create_access_token(data:dict)-> str:
    to_encode = data.copy()

    expire_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)

    to_encode.update({'exp' : expire_time})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt