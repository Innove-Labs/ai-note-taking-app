from typing import Optional

from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from starlette.requests import Request

from models import  User

from configs.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Assuming the payload has a 'sub' (subject) or 'user_id' field that identifies the user
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        return user_email  # Return the user object
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def get_current_user(request: Request) -> User:
    token: Optional[str] = None

    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization:
        token = authorization.split(" ")[-1]  # Token after "Bearer"

    if token is None:
        token = request.cookies.get("access_token")  # Adjust the cookie name as needed

    if token is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    user_email = decode_token(token)
    user = await User.find_one(email=user_email)

    if not user:
        raise HTTPException(status_code=401, detail="Not Authorized")

    return user