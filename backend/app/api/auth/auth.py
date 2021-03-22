from typing import Any, Union, Optional
from pydantic import BaseModel
from datetime import timedelta
from fastapi import APIRouter, Body, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict

import uuid

from api.schemas.token import TokenPayload, TokenResponse
from api.auth.deps import get_token_payload, authenticate_user, create_access_token
from api.core.database import db
from api.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    """
    Custom auth endpoint to generate access token.

    It follows OAuth2 password grant_flow specification
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires # pylint: disable=no-member
    )
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=TokenPayload)
def inspect_token(token_payload: TokenPayload = Depends(get_token_payload)):
    """
    Custom auth endpoint to obtain information about the token.
    """
    return token_payload
