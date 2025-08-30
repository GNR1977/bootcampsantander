from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    class Config:
        env_file = ".env"

settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(sub: str, role: str) -> str:
    return create_token({"sub": sub, "role": role, "type": "access"}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def create_refresh_token(sub: str) -> str:
    return create_token({"sub": sub, "type": "refresh"}, settings.REFRESH_TOKEN_EXPIRE_MINUTES)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None