
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import APIRouter, Body, Form, Depends, Security, Header, HTTPException, File, UploadFile
from api.schemas.user import User
from api.schemas.subscription import SubscriptionState
from api.database import db
from api.config import settings
from fastapi.security import HTTPAuthorizationCredentials
from api.auth.deps import get_current_user, get_user_access_token, security
import uuid
from shutil import copyfileobj
from functools import reduce

router = APIRouter()


@router.get("/run", response_model=SubscriptionState)
async def run_subscription(
    token: HTTPAuthorizationCredentials = Security(security),
    user_id: User = Depends(get_current_user)
):
    """
    Initiates a subscription to the specified phone number
    """
    return SubscriptionState()
