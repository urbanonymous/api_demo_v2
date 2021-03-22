""" Dependencies needed for authentication """

from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Any, Union, List, Optional
from pydantic import BaseModel
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi import APIRouter, Body, Form, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime, timedelta

from api.schemas.token import TokenJWTPayload, TokenPayload
from api.schemas.user import User, UserInDB
from api.core.database import db
from api.core.config import settings
from api.core.database import get_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Union[UserInDB, bool]:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    payload.update({"exp": expire})
    # Add default values to the token payload and enforce the schema
    payload = dict(TokenJWTPayload(**payload))
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY,
                             algorithm=settings.HASHING_ALGORITHM)
    return encoded_jwt


async def get_token_payload(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                             settings.HASHING_ALGORITHM])
    except JWTError:
        raise credentials_exception

    return TokenPayload(**payload)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                             settings.HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)

    if user is None:
        raise credentials_exception
    return User(**dict(user))
